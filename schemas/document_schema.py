from pydantic import BaseModel, Field, Json
from uuid import UUID
from typing import Optional, Any
from datetime import datetime

class DocumentCreate(BaseModel):
  name: str = Field(..., title='Name', min_length=3, max_length=50)
  description: str = Field(..., title='Description', min_length=3, max_length=125)
  template_id: UUID = Field(..., title='Template ID')
  data: Json[Any] = Field(..., title='Data')

class DocumentUpdate(BaseModel):
  name: Optional[str]
  description: Optional[str]
  template_id: Optional[str]

class DocumentDetail(BaseModel):
  document_id: UUID
  name: str
  description: str
  template_id: str
  path: str
  created_at: datetime
  updated_at: datetime
