from typing import List
from uuid import UUID
from models.user_model import User
from models.document_model import Document
from schemas.document_schema import DocumentCreate, DocumentUpdate

class DocumentService:
  @staticmethod
  async def list_documents(user: User) -> List[Document]:
    documents = await Document.find(Document.owner.id == user.id).to_list()
    return documents
  
  @staticmethod
  async def create_document(user: User, data: DocumentCreate) -> Document:
    document = Document(**data.model_dump(), owner=user)
    await document.insert()
    return document
  
  @staticmethod
  async def detail(user: User, document_id: UUID) -> Document | None:
    document = await Document.find_one(Document.document_id == document_id, Document.owner.id == user.id)
    return document
  
  @staticmethod
  async def update_document(user: User, document_id: UUID, data: DocumentUpdate) -> Document:
    document = await DocumentService.detail(user, document_id)
    await document.update({
      '$set': data.model_dump(exclude_unset=True)
    })
    await document.save()
    return document
  
  @staticmethod
  async def delete_document(user: User, document_id: UUID) -> None:
    document = await DocumentService.detail(user, document_id)
    if document:
      await document.delete()
