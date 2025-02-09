from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from models.user_model import User
from jose import jwt
from core.config import settings
from core.security import verify_password
from schemas.auth_schema import TokenPayload
from datetime import datetime
from pydantic import ValidationError
from typing import Optional
from services.user_service import UserService

oauth_reusavel = OAuth2PasswordBearer(
  tokenUrl=f'{settings.API_V1_STR}/auth/login',
  scheme_name='JWT'
)

auth_header = {'WWW-Authenticate': 'Bearer'}

async def authenticate(email: str, password: str) -> Optional[User]:
  user = await UserService.get_user_by_email(email=email)
  
  if not user:
    return None
  if not verify_password(
    password=password,
    hashed_password=user.hash_password
  ):
    return None
  
  return user

async def current_user(token: str = Depends(oauth_reusavel)) -> User:
  try:
    payload = jwt.decode(
      token,
      settings.JWT_SECRET_KEY,
      settings.ALGORITHM
    )
    
    token_data = TokenPayload(**payload)

    if datetime.fromtimestamp(token_data.exp) < datetime.now():
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Expired token',
        headers=auth_header
      )

  except(jwt.JWTError, ValidationError):
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail='Error in token validation',
      headers=auth_header
    )
  
  user = await UserService.get_user_by_id(token_data.sub)

  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='User not found',
      headers=auth_header
    )
  
  return user
