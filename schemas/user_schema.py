from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class UserAuth(BaseModel):
  email: EmailStr = Field(..., description='User\'s email')
  username: str = Field(
    ...,
    min_length=5,
    max_length=50,
    description='Username'
  )
  password: str = Field(
    ...,
    min_length=5,
    max_length=20,
    description='User\'s password'
  )

class UserDetail(BaseModel):
  user_id: UUID
  username: str
  email: EmailStr
