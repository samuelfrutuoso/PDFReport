from pydantic import BaseModel, Field, Json
from uuid import UUID
from typing import Optional, Any
from datetime import datetime

class DocumentCreate(BaseModel):
  name: str = Field(..., title='Name', min_length=3, max_length=50)
  description: str = Field(..., title='Description', min_length=3, max_length=125)
  template: UUID = Field(..., title='Template ID')
  data: Json[Any] = Field(..., title='Data')

class DocumentUpdate(BaseModel):
  name: Optional[str]
  description: Optional[str]
  template: Optional[str]

class DocumentDetail(BaseModel):
  document_id: UUID
  name: str
  description: str
  template: str
  # download_link: str
  created_at: datetime
  updated_at: datetime
