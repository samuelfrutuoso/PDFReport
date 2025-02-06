from fastapi import APIRouter
from api.api_v1.handlers import user, template
from api.auth.jwt import auth_router

router = APIRouter()

router.include_router(
  router=user.user_router,
  prefix='/users',
  tags=['users']
)

router.include_router(
  router=auth_router,
  prefix='/auth',
  tags=['auth']
)

router.include_router(
  router=template.template_router,
  prefix='/template',
  tags=['template']
)
