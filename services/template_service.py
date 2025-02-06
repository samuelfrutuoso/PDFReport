from models.user_model import User
from models.template_model import Template
from typing import List
from schemas.template_schema import TemplateCreate
from uuid import UUID

class TemplateService:
  @staticmethod
  async def list_services(user: User) -> List[Template]:
    templates = await Template.find(Template.owner.id == user.id).to_list()
    return templates
  
  @staticmethod
  async def create_template(user: User, data: TemplateCreate) -> Template:
    # template = Template(**data.model_dump(), owner=Link(user, User))
    template = Template(**data.model_dump(), owner=user)
    return await template.insert()
  
  @staticmethod
  async def detail(user: User, template_id: UUID) -> Template:
    template = await Template.find_one(Template.template_id == template_id, Template.owner.id == user.id)
    return template
