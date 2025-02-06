from fastapi import APIRouter, HTTPException, status
from beanie.exceptions import RevisionIdWasChanged
from schemas.user_schema import UserAuth, UserDetail
from services.user_service import UserService

user_router = APIRouter()

@user_router.post('/add',
                  summary='Add new user',
                  response_model=UserDetail)
async def add_user(data: UserAuth):
  try:
    return await UserService.create_user(data)
  except RevisionIdWasChanged:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail='Username or email already exists'
    )
  except Exception as err:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Unexpected {err=}, {type(err)=}"
    )
