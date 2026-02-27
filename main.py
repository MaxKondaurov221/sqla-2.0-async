import asyncio

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

import config
from models.base import Base


async def main():
    engine = create_async_engine(
        url = config.DB_URL,
        echo=config.DB_ECHO,
    )
    # Base.metadata.drop_all(engine)
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(main())