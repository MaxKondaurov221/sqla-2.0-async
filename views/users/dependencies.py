from fastapi import HTTPException
from fastapi.params import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.models import db_helper
from . import crud


async def get_user_by_id_or_raise(user_id: Annotated[int, Path],session: Annotated[AsyncSession, Depends(db_helper.get_session_dependency)]):
    user = await crud.get_user_by_id(session=session, user_id=user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail='User not found')