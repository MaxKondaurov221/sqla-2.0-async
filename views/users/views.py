from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from utils.email_sender import send_email
from views.users.schemas import UserSchema, UserSchemaUpdate, UserSchemaIn
from . import crud
from .dependencies import get_user_by_id_or_raise

router = APIRouter(tags=['users'])

@router.get('/', response_model=list[UserSchema])
async def get_users_list(session: Annotated[AsyncSession,Depends(db_helper.get_session_dependency)] ):
    return await crud.get_users(session = session)

@router.post('/', response_model=UserSchema)
async def create_user(
    background_tasks: BackgroundTasks,
    # session: Annotated[AsyncSession, Depends(db_helper.get_session_dependency)],
    data_create: UserSchema,
    session: AsyncSession = Depends(db_helper.get_session_dependency),
):
    user = await crud.create_user(
        session=session,
        data_create = data_create,
    )
    background_tasks.add_task(
        send_email,
        user.email,
        f"Hello dear {user.username}",
        text="Welcome message.",
    )
    return user


@router.get('/{user_id}', response_model=UserSchema)
async def get_users_by_id(user: User = Depends(get_user_by_id_or_raise)):
    return user

@router.patch('/{user_id}', response_model=UserSchema)
async def user_update(user_update: UserSchemaUpdate,user:User = Depends(get_user_by_id_or_raise),session: AsyncSession = Depends(db_helper.get_session_dependency)):
    return await crud.update_user_partial(session = session, user = user, user_update = user_update)