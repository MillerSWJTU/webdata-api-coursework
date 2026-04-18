from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Web Data API Coursework"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///./app.db"
    api_key: str = Field(default="xjco3011-secret-key", validation_alias="API_KEY", strip_whitespace=True)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )


settings = Settings()
