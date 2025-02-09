from fastapi import UploadFile
from models.user_model import User
from models.template_model import Template
from typing import List
from schemas.template_schema import TemplateCreate, TemplateUpdate
from uuid import UUID
import shutil
import os.path
import os
from core.config import settings

# TODO: Add content check: only index.html, images and css
# TODO: Add Upload to AWS S3 and others
def upload_template(file: UploadFile, template_id: str):
  template_path = os.path.join(settings.PATH_TEMPLATES, f'{template_id}.zip')
  with open(template_path, 'wb') as buffer:
    shutil.copyfileobj(file.file, buffer)

class TemplateService:
  @staticmethod
  async def list_services(user: User) -> List[Template]:
    templates = await Template.find(Template.owner.id == user.id).to_list()
    return templates
  
  @staticmethod
  async def create_template(user: User, data: TemplateCreate, file: UploadFile) -> Template:
    template = Template(**data.model_dump(), owner=user)
    await template.insert()
    upload_template(file, template.id)
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
    upload_template(file, template.id)
    return template
  
  @staticmethod
  async def delete_template(user: User, template_id: UUID) -> None:
    template = await TemplateService.detail(user, template_id)
    if template:
      await template.delete()
      # TODO: Add delete from AWS S3 and others
      template_path = os.path.join(settings.PATH_TEMPLATES, f'{template_id}.zip')
      if os.path.exists(template_path):
        os.remove(template_path)
