from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class TemplateCreate(BaseModel):
  name: str = Field(..., title='Name', min_length=3, max_length=50)
  description: str = Field(..., title='Description', min_length=3, max_length=50)
  # html: str = Field(..., title='HTML')
  # css: str = Field(..., title='CSS')
  # bootstrap: Optional[bool]

class TemplateUpdate(BaseModel):
  name: Optional[str]
  description: Optional[str]
  # html: Optional[str]
  # css: Optional[str]
  # bootstrap: Optional[str]

class TemplateSummary(BaseModel):
  template_id: UUID
  name: str
  description: str
  created_at: datetime
  updated_at: datetime

class TemplateDetail(BaseModel):
  template_id: UUID
  name: str
  description: str
  # html: str
  # css: str
  # bootstrap: bool
  created_at: datetime
  updated_at: datetime
