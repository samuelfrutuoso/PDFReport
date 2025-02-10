from typing import List, Dict, Any
from uuid import UUID
from models.user_model import User
from models.document_model import Document
from schemas.document_schema import DocumentCreate, DocumentUpdate
from models.document_model import Template
from core.config import settings
from fastapi import Depends, HTTPException, status
import os.path

async def create_pdf(user_id: str, template_id: str, document_id: str, data: object):
  document_path = settings.DOCUMENTS_DIR / f'/{document_id}.pdf'
  download_link = f'/{settings.API_V1_STR}/documents/{document_id}/download'
  # TODO: Extract all from zip path and genereate PDF

class DocumentService:
  @staticmethod
  async def list_documents(user: User) -> List[Document]:
    documents = await Document.find(Document.owner.id == user.id).to_list()
    return documents
  
  @staticmethod
  async def create_document(user: User, data: DocumentCreate) -> Document:
    document = Document(**data.model_dump(), owner=user)
    await document.insert()
    await create_pdf(user.id, document.template_id, document.id, data.data)
    return document
  
  @staticmethod
  async def detail(user: User, document_id: UUID) -> Document | None:
    document = await Document.find_one(Document.document_id == document_id, Document.owner.id == user.id)
    return document
  
  # TODO: Download document
  @staticmethod
  async def download(user: User, document_id: UUID):
    document = await DocumentService.detail(user, document_id)
    if not document:
      raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail='File not found',
        headers=settings.HTTP_AUTH_HEADER
      )
    document_path = settings.DOCUMENTS_DIR / f'{document_id}.pdf'
    if not os.path.isfile(document_path):
      raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail='File not found',
        headers=settings.HTTP_AUTH_HEADER
      )
  
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
