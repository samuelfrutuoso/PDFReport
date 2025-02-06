from beanie import Document, Indexed
from uuid import UUID, uuid4
from pydantic import Field
from datetime import datetime
from typing import Optional

class Document(Document):
  pdf_id: UUID = Field(default_factory=uuid4, unique=True)
  name: str = Indexed(str, unique=True)
  desabled: Optional[str] = None

  def __repr__(self):
    return f'{self.pdf_id} {self.name}.pdf'
  
  def __str__(self):
    return f'{self.pdf_id} {self.name}.pdf'
  
  def __eq__(self, other: object) -> bool:
    if isinstance(other, Pdf):
      return self.pdf_id == other.pdf_id
    return False
  
  @property
  def create(self) -> datetime:
    return self.id.generation_time
