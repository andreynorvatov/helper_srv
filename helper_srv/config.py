from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    PROJECT_NAME : str= "Helper"
    API_V1_STR: str = "/api/v1"

    OPENROUTER_CREDITS_API: str = Field(default="https://openrouter.ai/api/v1/credits")
    OPENROUTER_API_KEY: str = Field(default="", description="API ключ")

    CBR_API: HttpUrl = Field(default="https://www.cbr.ru/scripts/XML_daily.asp?date_req=")


settings = Settings()  # type: ignore
