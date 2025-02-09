from beanie import Document, Indexed
from uuid import UUID, uuid4
from pydantic import Field, EmailStr
from datetime import datetime
from typing import Optional

class User(Document):
  user_id: UUID = Field(default_factory=uuid4)
  username: str = Indexed(str, unique=True)
  email: EmailStr = Indexed(EmailStr, unique=True)
  hash_password: str
  name: Optional[str] = None
  desabled: Optional[str] = None

  class Settings:
    collection = 'users'

  def __repr__(self):
    return f'User {self.email}'
  
  def __str__(self):
    return f'User {self.email}'
  
  def __eq__(self, other: object) -> bool:
    if isinstance(other, User):
      return self.email == other.email
    return False
  
  @property
  def create(self) -> datetime:
    return self.id.generation_time
  
  @classmethod
  async def by_email(self, email: str) -> "User":
    return await self.find_one(self.email == email)
