from fastapi import APIRouter, HTTPException
import httpx

from config import settings

openrouter_router = APIRouter()



async def _fetch_credits() -> dict:
    """Внутренний запрос к /api/v1/credits."""
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Accept": "application/json",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(settings.OPENROUTER_CREDITS_API, headers=headers)
        resp.raise_for_status()
        return resp.json()


@openrouter_router.get("/credits")
async def get_credits():
    try:
        return await _fetch_credits()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text,
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=str(e))


