from pydantic import AnyHttpUrl, field_validator
from typing import Optional
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    app_name: str = "Staff Eats Project"
    version: str = "1.0.0"

    # Token expiration settings
    refresh_token_expire_minutes: int = 60 * 24 * 10
    access_token_expire_minutes: int = 60 * 24 * 10

    # Environment variables
    jwt_secret_key: Optional[str] = os.getenv("JWT_SECRET_KEY")
    base_url: Optional[str] = os.getenv("BASE_URL")
    jwt_refresh_secret_key: Optional[str] = os.getenv("JWT_REFRESH_SECRET_KEY")
    jwt_algorithm: str = os.getenv("ALGORITHM", "HS256")
    bottoken: Optional[str] = os.getenv("BOT_TOKEN")
    hrbot_token: Optional[str] = os.getenv("HRBOT_TOKEN")
    login_iiko: Optional[str] = os.getenv("LOGIN_IIKO")
    password_iiko: Optional[str] = os.getenv("PASSWORD_IIKO")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    backend_pass: Optional[str] = os.getenv("BACKEND_PASS")
    front_url: Optional[str] = os.getenv("FRONT_URL")
    INTERNAL_BASE_URL:str = "https://api.service.safiabakery.uz/"
    INTERNAL_FRONT_URL:str = "https://admin.service.safiabakery.uz/"
    sizes:list = [
        'XS (42 - 44)',
        'S (46 - 48)',
        'M (50 - 52)',
        'L (54 - 56)',
        'XL (58 - 60)',
        'XXL (62 - 64)',
        'XXXL (66 - 68)'
    ]

    # Security settings



# Initialize settings
settings = Settings()
