from typing import List
from decouple import config
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
  API_V1_STR: str = '/api/v1'
  JWT_SECRET_KEY: str = config('JWT_SECRET_KEY', cast=str)
  JWT_REFRESH_SECRET_KEY: str = config('JWT_REFRESH_SECRET_KEY', cast=str)
  ALGORITHM: str = 'HS256'
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
  ACCESS_TOKEN_REFRESH_MINUTES: int = 60 * 24 * 7
  BACKEND_CORS_ORIGNS: List[AnyHttpUrl] = [] # List of IP Address accepted to connect
  PROJECT_NAME: str = 'PDFReport'
  BASE_DIR: Path = Path(__file__).resolve().parent.parent
  TEMPLATES_DIR: Path = BASE_DIR / 'writable' / 'templates'
  DOCUMENTS_DIR: Path = BASE_DIR / 'writable' / 'documents'
  HTTP_AUTH_HEADER: dict[str, str] = {'WWW-Authenticate': 'Bearer'}

  # Database
  MONGO_CONNECTION_STRING: str = config('MONGO_CONNECTION_STRING', cast=str)

  class Config:
    case_sensitive = True

  def __init__(self):
    BaseSettings.__init__(self)
    self.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    self.DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

settings = Settings()
