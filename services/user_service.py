from models.user_model import User
from schemas.user_schema import UserAuth
from core.security import get_password
from typing import Optional
from uuid import UUID

class UserService:
  @staticmethod
  async def create_user(user_auth: UserAuth):
    new_user = User(
      username=user_auth.username,
      email=user_auth.email,
      hash_password=get_password(user_auth.password)
    )
    await new_user.save()
    return new_user
  
  @staticmethod
  async def get_user_by_email(email: str) -> Optional[User]:
    user = await User.find_one(User.email == email)
    return user
  
  @staticmethod
  async def get_user_by_id(id: UUID) -> Optional[User]:
    user = await User.find_one(User.user_id == id)
    return user
