from fastapi import FastAPI
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

app.include_router(
  router,
  prefix=settings.API_V1_STR
)
