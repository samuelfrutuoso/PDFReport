from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from services.user_service import UserService
from core.security import create_access_token, create_refresh_token
from schemas.auth_schema import TokenSchema
from schemas.user_schema import UserDetail
from models.user_model import User
from api.dependencies.auth_deps import current_user, authenticate

auth_router = APIRouter()

@auth_router.post('/login',
                  summary='Create Access Token and Refresh Token',
                  response_model=TokenSchema)
async def login(data: OAuth2PasswordRequestForm = Depends()) -> Any:
  user = await authenticate(
    email=data.username,
    password=data.password
  )

  if not user:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail='Wrong email or password'
    )
  
  token = TokenSchema(
    access_token=create_access_token(user.user_id),
    refresh_token=create_refresh_token(user.user_id)
  )

  return token
