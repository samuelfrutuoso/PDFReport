from typing import List
from uuid import UUID
from models.user_model import User
from models.document_model import Document
from schemas.document_schema import DocumentCreate, DocumentUpdate
from core.config import settings
from fastapi import HTTPException, status
from .template_service import get_template_path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

get_document_path = lambda document: settings.DOCUMENTS_DIR / f'{document.id}.pdf'

class DocumentService:
  @staticmethod
  async def list_documents(user: User) -> List[Document]:
    documents = await Document.find(Document.owner.ref.id == user.id).to_list()
    return documents
  
  @staticmethod
  async def create_document(user: User, data: DocumentCreate) -> Document:
    document = Document(**data.model_dump(), owner=user)
    
    template_path = get_template_path(document.template)
    html_file = template_path / 'index.html'
    document_path = get_document_path(document)

    if not template_path.is_dir() or not html_file.is_file():
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Template not found',
        headers=settings.HTTP_AUTH_HEADER
      )
    
    env = Environment(loader=FileSystemLoader(settings.TEMPLATES_DIR))
    template = env.get_template(f'{document.template.ref.id}.html')
    html = template.render(data)
    HTML(string=html).write_pdf(document_path)

    await document.insert()
    return document
  
  @staticmethod
  async def detail(user: User, document_id: UUID) -> Document | None:
    document = await Document.find_one(Document.document_id == document_id, Document.owner.ref.id == user.id)
    return document
  
  @staticmethod
  async def download(user: User, document_id: UUID) -> dict[str, str]:
    document = await DocumentService.detail(user, document_id)

    if not document:
      raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail='Document not found',
        headers=settings.HTTP_AUTH_HEADER
      )
    
    document_file = get_document_path(document)
    if not document_file.is_file():
      raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail='File template not found',
        headers=settings.HTTP_AUTH_HEADER
      )
    
    return {'path': document_file, 'name': f'{document.name}.pdf'}
  
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
