from models.user_model import User
from models.template_model import Template
from typing import List
from schemas.template_schema import TemplateCreate, TemplateUpdate
from uuid import UUID

class TemplateService:
  @staticmethod
  async def list_services(user: User) -> List[Template]:
    templates = await Template.find(Template.owner.id == user.id).to_list()
    return templates
  
  # TODO: Add save zip file and set template.template_path
  @staticmethod
  async def create_template(user: User, data: TemplateCreate) -> Template:
    template = Template(**data.model_dump(), owner=user)
    await template.insert()
    return template
  
  @staticmethod
  async def detail(user: User, template_id: UUID) -> Template | None:
    template = await Template.find_one(Template.template_id == template_id, Template.owner.id == user.id)
    return template
  
  # TODO: Add save zip file and set template.template_path
  @staticmethod
  async def update_template(user: User, template_id: UUID, data: TemplateUpdate) -> Template:
    template = await TemplateService.detail(user, template_id)
    await template.update({
      '$set': data.model_dump(exclude_unset=True)
    })
    await template.save()
    return template
  
  # TODO: Add delete template file
  @staticmethod
  async def delete_template(user: User, template_id: UUID) -> None:
    template = await TemplateService.detail(user, template_id)
    if template:
      await template.delete()
