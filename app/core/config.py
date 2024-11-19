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
    jwt_algorithm: Optional[str] = os.getenv("ALGORITHM",'HS256')
    bottoken: Optional[str] = os.getenv("BOT_TOKEN", "6247686133:AAG-7Z9ZMpaEanMd1VlyiKO4S2Xbm_jp8BE")
    # bottoken: Optional[str] = os.getenv("BOT_TOKEN", "7899102795:AAHp9W4xycI3u_iAZOFLkC4I9Xa9N1aQYaw")
    hrbot_token: Optional[str] = os.getenv("HRBOT_TOKEN")
    login_iiko: Optional[str] = os.getenv("LOGIN_IIKO")
    password_iiko: Optional[str] = os.getenv("PASSWORD_IIKO")
    database_url: Optional[str] = os.getenv("DATABASE_URL")
    backend_pass: Optional[str] = os.getenv("BACKEND_PASS")
    front_url: Optional[str] = os.getenv("FRONT_URL")
    MICROSERVICE_BASE_URL: Optional[str] = os.getenv("MICROSERVICE_BASE_URL")
    MICROSERVICE_USERNAME: Optional[str]= os.getenv("MICROSERVICE_USERNAME")
    MICROSERVICE_PASSWORD: Optional[str] = os.getenv("MICROSERVICE_PASSWORD")
    BASE_URL: Optional[str] = "https://api.service.safiabakery.uz/"
    # FRONT_URL: Optional[str] = "https://admin.service.safiabakery.uz/"
    FRONT_URL: Optional[str] = 'https://service.safiabakery.uz/'
    IT_SUPERGROUP: int = os.getenv("IT_SUPERGROUP")
    sizes: list = [
        'XS (42 - 44)',
        'S (46 - 48)',
        'M (50 - 52)',
        'L (54 - 56)',
        'XL (58 - 60)',
        'XXL (62 - 64)',
        'XXXL (66 - 68)'
    ],
    SCHEDULER_DATABASE_URL: Optional[str] = os.getenv("SCHEDULER_DATABASE_URL")

    # Security settings
    class Config:
        env_file = '.env'
        extra ='allow'


# Initialize settings
settings = Settings()
