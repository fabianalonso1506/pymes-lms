import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str = "/api"
    secret_key: str = os.getenv("SECRET_KEY", "secret")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")


settings = Settings()
