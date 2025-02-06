from beanie import Document, Indexed, Link, before_event, Replace, Insert
from uuid import UUID, uuid4
from pydantic import Field
from datetime import datetime, timezone
from typing import Optional
from .user_model import User

class Template(Document):
  template_id: UUID = Field(default_factory=uuid4, unique=True)
  name: str = Indexed(str)
  description: Optional[str] = None
  owner: Link[User]
  # html: str
  # css: str
  # bootstrap: Optional[bool] = False
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

  def __repr__(self) -> str:
    return f'Template {self.name}'
  
  def __str__(self) -> str:
    return self.name
  
  def __hash__(self) -> int:
    return hash(self.name)
  
  def __eq__(self, other: object) -> bool:
    if isinstance(other, Template):
      return self.template_id == other.template_id
    return False
  
  @before_event([Replace, Insert])
  def sync_update_at(self):
    self.updated_at = datetime.now(timezone.utc)
