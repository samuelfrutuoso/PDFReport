from beanie import Document, Indexed, Link, before_event, Replace, Insert
from uuid import UUID, uuid4
from pydantic import Field
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from .template_model import Template
from .user_model import User

class Document(Document):
  document_id: UUID = Field(default_factory=uuid4, unique=True)
  name: str = Indexed(str, unique=True)
  description: Optional[str] = None
  template_id: Link[Template]
  owner: Link[User]
  path: str
  data: Dict[str, Any]
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

  class Settings:
    collection = 'documents'

  def __repr__(self):
    return f'Document {self.document_id} {self.name}.pdf'
  
  def __str__(self):
    return self.path
  
  def __eq__(self, other: object) -> bool:
    if isinstance(other, Document):
      return self.document_id == other.document_id
    return False
  
  @before_event([Insert])
  async def create_pdf(self):
    self.path = f'/{self.owner.id}/{self.id}.pdf'
    template = await Template.find_one(
      Template.template_id == self.template_id,
      Template.owner.id == self.owner.id
      )
    # TODO: Extract all from zip path and genereate PDF

  @before_event([Replace])
  def sync_update_at(self):
    self.updated_at = datetime.now(timezone.utc)
