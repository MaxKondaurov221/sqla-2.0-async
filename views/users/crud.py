import asyncio

from sqlalchemy import select, Sequence
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.engine import Result

from core.models import User, Post

import config
from views.users.schemas import UserSchemaIn


async def create_user(
        session: AsyncSession,
        data_create: UserSchemaIn
):
    user = User(
        **data_create.model_dump()
    )
    async with session.begin():
        session.add(user)
    return user

async def get_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.execute(stmt)
    users = result.scalars().all()
    for user in users:
        print(user)
    return users

async def get_user_by_id(
        session: AsyncSession, user_id: int ) -> User | None:
    #stmt = select(User).where(User.id == user_id)
    user: User|None =  await session.get(User, user_id)
    print(f"user {user}")
    return user

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result:Result =await session.execute(stmt)
    user:User = result.scalars().one()
    print(f"user ---- {user}")
    return user


async def user_update(
        session: AsyncSession, user_id: int, data_update: UserSchemaIn ) -> User | None:
    data = data_update.model_dump(exclude_unset=True)
    if not data:
        return None
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user: User = result.scalars().one()

    for key, value in data.items():
        setattr(user, key, value)

    await session.commit()
    await session.refresh(user)

    return user





async def create_post_for_user(
        session: AsyncSession,
        user: User,
        *post_titles:str
) -> list[Post]:

    posts = [Post(title= title, author_id=user.id)
             for title in post_titles]
    print("ЭТО ПОСТЫ!", posts)
    async with session.begin_nested():
        session.add_all(posts)

    for post in posts:
        print(post)
    return posts


async def get_posts_with_user(session: AsyncSession) -> list[Post]:
    stmt = select(Post).options(joinedload(Post.author)).order_by(Post.id)
    result = await session.execute(stmt)
    posts = result.scalars().all()
    print(posts)
    for post in posts:
        print("*" * 7, post)
        print("_" * 7,post.author)
    return list(posts)

async def get_user_with_posts(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    result = await session.execute(stmt)
    users = result.unique().scalars().all()
    print(users)
    return users

# async def main():
#     async with async_session() as session:
#         # await create_user(
#         #     session,
#         #     'John'
#         # )
#         # await create_user(
        #     session,
        #     'Sam',
        #     email ='sam@com.com',
        #     motto = 'My Motto'
        # )
        # await create_user(
        #     session,
        #     'Alice'
        # )
        # await create_user(
        #     session,
        #     'Bob',
        #     email='bob@com.com',
        #     motto='My Motto'
        # )
        # await get_users(session)
        # await get_user_by_id(session, 1)
        # await get_user_by_id(session, 2)
        # sam: User = await get_user_by_username(session, 'Sam')
        # john: User = await get_user_by_username(session, 'John')
        # await create_post_for_user(session, john, "P1",'P2')
        # await create_post_for_user(session, sam, "P2",'P3')
        # await get_posts_with_user(session)
        # await get_user_with_posts(session)
