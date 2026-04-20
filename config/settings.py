from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Настройки приложения"""

    # Database
    database_url: str = Field(default="sqlite:///data/scraper.db")

    # Scraping
    request_timeout: int = Field(default=10)
    delay_between_requests: float = Field(default=1.0)
    max_retries: int = Field(default=3)

    # Sentiment Analysis
    sentiment_model: str = Field(
        default="blanchefort/rubert-base-cased-sentiment"
    )

    # Logging
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="logs/scraper.log")

    # Airflow
    airflow_dags_folder: str = Field(default="dags/")
    airflow_schedule_interval: str = Field(default="@daily")

    # Notifications
    slack_webhook_url: Optional[str] = None
    email_recipients: list = Field(default_factory=list)

    class Config:
        env_file = ".env"
        env_prefix = "SCRAPER_"


settings = Settings()