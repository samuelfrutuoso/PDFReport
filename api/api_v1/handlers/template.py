from fastapi import APIRouter, Depends
from schemas.template_schema import TemplateSummary, TemplateCreate, TemplateDetail
from models.user_model import User
from api.dependencies.user_deps import get_current_user
from services.template_service import TemplateService
from typing import List
from uuid import UUID

template_router = APIRouter()

@template_router.get('/',
                     summary='List all templates',
                     response_model=List[TemplateSummary])
async def list_templates(user: User = Depends(get_current_user)):
  return await TemplateService.list_services(user)

@template_router.get('/{template_id}',
                     summary='Template datail by ID',
                     response_model=TemplateDetail)
async def detail(template_id: UUID, user: User = Depends(get_current_user)):
  return await TemplateService.detail(user, template_id)

@template_router.post('/create',
                      summary='Add Template',
                      response_model=TemplateSummary)
async def create_template(data: TemplateCreate, user: User = Depends(get_current_user)):
  return await TemplateService.create_template(user, data)
