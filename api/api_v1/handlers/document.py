from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from typing import List, Annotated
from uuid import UUID
from api.dependencies.auth_deps import current_user
from schemas.document_schema import DocumentDetail, DocumentCreate, DocumentUpdate
from models.user_model import User
from services.document_service import DocumentService

document_router = APIRouter()

@document_router.get('/',
                     summary='List all documents',
                     response_model=List[DocumentDetail])
async def list_documents(user: Annotated[User, Depends(current_user)]):
  return await DocumentService.list_documents(user)

@document_router.get('/{document_id}',
                     summary='Document datail by ID',
                     response_model=DocumentDetail)
async def detail(document_id: UUID,
                 user: Annotated[User, Depends(current_user)]):
  return await DocumentService.detail(user, document_id)

@document_router.get('/{document_id}/download',
                     summary='Download document by ID',
                     response_model=DocumentDetail)
async def download(document_id: UUID,
                 user: Annotated[User, Depends(current_user)]):
  file = await DocumentService.download(user, document_id)
  return FileResponse(
    path=file.path,
    filename=file.name,
    media_type='application/pdf'
  )

@document_router.post('/create',
                      summary='Add document',
                      response_model=DocumentDetail)
async def create_template(data: DocumentCreate,
                          user: Annotated[User, Depends(current_user)]):
  return await DocumentService.create_document(user, data)

@document_router.put('/{document_id}',
                     summary='Update document',
                     response_model=DocumentDetail)
async def update(document_id: UUID,
                 data: DocumentUpdate,
                 user: Annotated[User, Depends(current_user)]):
  return await DocumentService.update_document(user, document_id, data)

@document_router.delete('/{document_id}',
                        summary='Delete document')
async def delete(document_id: UUID,
                 user: Annotated[User, Depends(current_user)]):
  await DocumentService.delete_document(user, document_id)
