from fastapi import UploadFile, HTTPException, status
from models.user_model import User
from models.template_model import Template
from typing import List
from schemas.template_schema import TemplateCreate, TemplateUpdate
from uuid import UUID
import shutil
from core.config import settings
import asyncio

get_template_path = lambda template_id: settings.TEMPLATES_DIR / f'{template_id}.zip'

class TemplateService:
  @staticmethod
  async def list_services(user: User) -> List[Template]:
    templates = await Template.find(Template.owner.id == user.id).to_list()
    return templates
  
  @staticmethod
  async def create_template(user: User, data: TemplateCreate) -> Template:
    template = Template(**data.model_dump(), owner=user)
    await template.insert()
    asyncio.create_task(TemplateService.cancel_template(user.user_id, template.template_id, 300))
    return template
  
  @staticmethod
  async def detail(user: User, template_id: UUID) -> Template | None:
    template = await Template.find_one(Template.template_id == template_id, Template.owner.id == user.id)
    return template
  
  @staticmethod
  async def update_template(user: User, template_id: UUID, data: TemplateUpdate, file: UploadFile) -> Template:
    template = await TemplateService.detail(user, template_id)
    await template.update({
      '$set': data.model_dump(exclude_unset=True)
    })
    await template.save()
    return template
  
  # TODO: Add content check: only index.html, images and css
  # TODO: Add Upload to AWS S3 and others
  @staticmethod
  async def upload_template(user: User, template_id: UUID, file: UploadFile):
    template = await TemplateService.detail(user.user_id, template_id)
    if not template:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Template not found',
        headers=settings.HTTP_AUTH_HEADER
      )
    
    template_path = get_template_path(template_id)
    with open(template_path, 'wb') as buffer:
      shutil.copyfileobj(file.file, buffer)
    
    template.file_uploaded = True
    template.save()
  
  @staticmethod
  async def delete_template(user: User, template_id: UUID) -> None:
    template = await TemplateService.detail(user, template_id)
    if template:
      await template.delete()
      # TODO: Add delete from AWS S3 and others
      template_path = get_template_path(template_id)
      template_path.unlink(missing_ok=True)
  
  @staticmethod
  async def cancel_template(user_id: UUID, template_id: UUID, delay: int) -> None:
    await asyncio.sleep(delay)

    template = await TemplateService.detail(user_id, template_id)
    
    if template and not template.file_uploaded:
      template.delete()
