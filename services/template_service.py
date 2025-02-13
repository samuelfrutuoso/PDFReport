from fastapi import UploadFile, HTTPException, status
from models.user_model import User
from models.template_model import Template
from typing import List
from schemas.template_schema import TemplateCreate, TemplateUpdate
from uuid import UUID
import shutil
from core.config import settings
import asyncio
from zipfile import ZipFile

get_template_path = lambda template: settings.TEMPLATES_DIR / f'{template.id}'

class TemplateService:
  @staticmethod
  async def list_services(user: User) -> List[Template]:
    templates = await Template.find(Template.owner.ref.id == user.id).to_list()
    return templates
  
  @staticmethod
  async def create_template(user: User, data: TemplateCreate) -> Template:
    template = Template(**data.model_dump(), owner=user)
    await template.insert()
    asyncio.create_task(TemplateService.cancel_template(user, template.template_id, 300))
    return template
  
  @staticmethod
  async def detail(user: User, template_id: UUID) -> Template | None:
    template = await Template.find_one(Template.template_id == template_id, Template.owner.ref.id == user.id)
    return template
  
  @staticmethod
  async def update_template(user: User, template_id: UUID, data: TemplateUpdate, file: UploadFile) -> Template:
    template = await TemplateService.detail(user, template_id)
    await template.update({
      '$set': data.model_dump(exclude_unset=True)
    })
    await template.save()
    return template
  
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
    
    try:
      temp_file = settings.TEMP_DIR / f'{template.id}.zip'

      # Save the zip file on temp folder
      with open(temp_file, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
      
      with ZipFile(temp_file) as temp_zip:
        # Check structure
        for filename in temp_zip.namelist():
          if not filename.endswith(settings.TEMPLATE_ACCEPTED_EXTENSIONS):
            raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail='Wrong template structure',
              headers=settings.HTTP_AUTH_HEADER
            )
       
       # Extract all files
        template_path = get_template_path(template.id)
        if template_path.exists():
          template_path.unlink()
        
        template_path.mkdir()
        temp_zip.extractall(template_path)
    
    except Exception:
      raise
    else:
      template.file_uploaded = True
      template.save()
    finally:
      temp_file.unlink()
  
  @staticmethod
  async def delete_template(user: User, template_id: UUID) -> None:
    template = await TemplateService.detail(user, template_id)
    if template:
      # TODO: Add delete from AWS S3 and others
      template_path = get_template_path(template.id)
      template_path.unlink(missing_ok=True)
      await template.delete()
  
  @staticmethod
  async def cancel_template(user: User, template_id: UUID, delay: int) -> None:
    await asyncio.sleep(delay)

    template = await TemplateService.detail(user, template_id)
    
    if template and not template.file_uploaded:
      template.delete()
