from pathlib import Path
from pydantic_settings import BaseSettings

ENV_FILE = Path(__file__).parent / ".env"

class Settings(BaseSettings):
    database_url: str
    gemini_api_key: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    secret_key: str
    github_token: str
    github_username: str

    class Config:
        env_file = ENV_FILE

settings = Settings()