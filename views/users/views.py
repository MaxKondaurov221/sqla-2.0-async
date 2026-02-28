from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from views.users.schemas import UserSchema, UserSchemaIn
from . import crud

router = APIRouter(tags=['users'])

@router.get('/', response_model=list[UserSchema])
async def get_users_list(session: AsyncSession = Depends(db_helper.get_session_dependency)):
    return await crud.get_users(session = session)

@router.post('/', response_model=UserSchema)
async def create_user(data_create: UserSchemaIn,session: AsyncSession = Depends(db_helper.get_session_dependency)):
    return await crud.create_user(session = session, data_create = data_create)


@router.get('/{user_id}', response_model=UserSchema)
async def get_users_by_id(user_id:int, session: AsyncSession = Depends(db_helper.get_session_dependency)):
    return await crud.get_user_by_id(session = session, user_id = user_id)

@router.patch('/{user_id}', response_model=UserSchema)
async def user_update(data_update: UserSchemaIn, user_id: int, session: AsyncSession = Depends(db_helper.get_session_dependency)):
    return await crud.user_update(session = session, user_id = user_id, data_update = data_update)