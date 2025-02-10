from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class TemplateCreate(BaseModel):
  name: str = Field(..., title='Name', min_length=3, max_length=50)
  description: str = Field(..., title='Description', min_length=3, max_length=125)
  bootstrap: Optional[bool]

class TemplateUpdate(BaseModel):
  name: Optional[str]
  description: Optional[str]
  bootstrap: Optional[str]

class TemplateSummary(BaseModel):
  template_id: UUID
  name: str
  description: str
  file_uploaded: bool
  bootstrap: bool
  created_at: datetime
  updated_at: datetime

class TemplateDetail(BaseModel):
  template_id: UUID
  name: str
  description: str
  file_uploaded: bool
  bootstrap: bool
  created_at: datetime
  updated_at: datetime
