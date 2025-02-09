from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class TemplateCreate(BaseModel):
  name: str = Field(..., title='Name', min_length=3, max_length=50)
  description: str = Field(..., title='Description', min_length=3, max_length=125)
  template_path: str = Field(..., title='ZIP Content')
  bootstrap: Optional[bool]

class TemplateUpdate(BaseModel):
  name: Optional[str]
  description: Optional[str]
  template_path: Optional[str]
  bootstrap: Optional[str]

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
  template_path: str
  bootstrap: bool
  created_at: datetime
  updated_at: datetime
