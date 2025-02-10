from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from contextlib import asynccontextmanager
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

# Models
from models.user_model import User
from models.document_model import Document
from models.template_model import Template

# Routers
from api.api_v1.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
  # Starting app
  client_db = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).pdfreport

  await init_beanie(
    database=client_db,
    document_models=[
      Document,
      Template,
      User,
    ]
  )

  yield
  # Shuting down app

app = FastAPI(
  title=settings.PROJECT_NAME,
  openapi_url=f'{settings.API_V1_STR}/openapi.json',
  lifespan=lifespan
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.BACKEND_CORS_ORIGNS,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)

app.include_router(
  router,
  prefix=settings.API_V1_STR
)
