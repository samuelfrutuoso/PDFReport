from fastapi import APIRouter, Depends, UploadFile, File, Form
from schemas.template_schema import TemplateSummary, TemplateCreate, TemplateDetail, TemplateUpdate
from models.user_model import User
from api.dependencies.auth_deps import current_user
from services.template_service import TemplateService
from typing import List, Annotated
from uuid import UUID

template_router = APIRouter()

@template_router.get('/',
                     summary='List all templates',
                     response_model=List[TemplateSummary])
async def list_templates(user: Annotated[User, Depends(current_user)]):
  return await TemplateService.list_services(user)

@template_router.get('/{template_id}',
                     summary='Template datail by ID',
                     response_model=TemplateDetail)
async def detail(template_id: UUID,
                 user: Annotated[User, Depends(current_user)]):
  return await TemplateService.detail(user, template_id)

@template_router.post('/create',
                      summary='Add template',
                      response_model=TemplateSummary)
async def create_template(data: TemplateCreate,
                          user: Annotated[User, Depends(current_user)]):
  return await TemplateService.create_template(user, data)

@template_router.post('/upload{template_id}',
                      summary='Upload template',
                      response_model=TemplateSummary)
async def upload_template(template_id: UUID,
                          file: Annotated[UploadFile, File(media_type='application/zip')],
                          user: Annotated[User, Depends(current_user)]):
  return await TemplateService.upload_template(user, template_id, file)

@template_router.put('/{template_id}',
                     summary='Update template',
                     response_model=TemplateDetail)
async def update(template_id: UUID, data: TemplateUpdate,
                 user: Annotated[User, Depends(current_user)]):
  return await TemplateService.update_template(user, template_id, data)

@template_router.delete('/{template_id}',
                        summary='Delete template')
async def delete(template_id: UUID,
                 user: Annotated[User, Depends(current_user)]):
  await TemplateService.delete_template(user, template_id)
