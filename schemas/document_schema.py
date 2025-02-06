from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class DocumentSchema(BaseModel):
  pdf_id: UUID = Field(default_factory=uuid4)
  template_name: str
  data: dict # Carregar modelo do banco ou arquivo
