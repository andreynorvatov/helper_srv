from fastapi import APIRouter, HTTPException
import httpx
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
import xml.etree.ElementTree as ET

from config import settings

currency_router = APIRouter()

# Модель ответа
class CurrencyRateResponse(BaseModel):
    pair: str
    rate: float
    date: str
    source: str


# Функция для получения курса USD/RUB с сайта ЦБ РФ
async def get_cbr_rate(date: Optional[str] = None) -> float:
    """
    Получает курс USD/RUB с сайта Центрального Банка РФ
    """
    if not date:
        date = datetime.now().strftime("%d/%m/%Y")

    # Парсим дату для формирования запроса
    try:
        parsed_date = datetime.strptime(date, "%d/%m/%Y")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты. Используйте DD/MM/YYYY")

    # URL для получения курсов с ЦБ РФ
    url = f"{settings.CBR_API}{date}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

            # Парсим XML ответ
            root = ET.fromstring(response.content)

            # Ищем USD
            for valute in root.findall('Valute'):
                char_code = valute.find('CharCode')
                if char_code is not None and char_code.text == 'USD':
                    value = valute.find('Value')
                    if value is not None:
                        # Заменяем запятую на точку и конвертируем в float
                        rate = float(value.text.replace(',', '.'))
                        return rate

            raise HTTPException(status_code=404, detail="Курс USD не найден")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Ошибка при обращении к API ЦБ РФ: {str(e)}")
    except ET.ParseError:
        raise HTTPException(status_code=500, detail="Ошибка парсинга ответа от ЦБ РФ")


@currency_router.get("/usd-rub", response_model=CurrencyRateResponse)
async def get_usd_rub_rate(date: Optional[str] = None):
    """
    Получить курс USD/RUB

    Параметры:
    - date: дата в формате DD/MM/YYYY (опционально, по умолчанию сегодня)

    Пример: GET /api/currency/usd-rub?date=15/09/2026
    """
    try:
        rate = await get_cbr_rate(date)

        # Если дата не указана, используем сегодняшнюю
        if not date:
            date = datetime.now().strftime("%d/%m/%Y")

        return CurrencyRateResponse(
            pair="USD/RUB",
            rate=rate,
            date=date,
            source="Центральный Банк РФ (cbr.ru)"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")
