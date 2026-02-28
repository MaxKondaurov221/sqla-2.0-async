from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from views.users.schemas import UserSchema, UserSchemaUpdate, UserSchemaIn
from . import crud
from .dependencies import get_user_by_id_or_raise

router = APIRouter(tags=['users'])

@router.get('/', response_model=list[UserSchema])
async def get_users_list(session: Annotated[AsyncSession,Depends(db_helper.get_session_dependency)] ):
    return await crud.get_users(session = session)

@router.post('/', response_model=UserSchema)
async def create_user(data_create: UserSchemaIn,session: Annotated[AsyncSession,Depends(db_helper.get_session_dependency)]):
    return await crud.create_user(session = session, data_create = data_create)


@router.get('/{user_id}', response_model=UserSchema)
async def get_users_by_id(user: User = Depends(get_user_by_id_or_raise)):
    return user

@router.patch('/{user_id}', response_model=UserSchema)
async def user_update(user_update: UserSchemaUpdate,user:User = Depends(get_user_by_id_or_raise),session: AsyncSession = Depends(db_helper.get_session_dependency)):
    return await crud.update_user_partial(session = session, user = user, user_update = user_update)