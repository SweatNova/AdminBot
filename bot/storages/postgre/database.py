from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from contextlib import asynccontextmanager
from .models import Base
from bot.config_reader import get_config, BotConfig

bot_config = get_config(model=BotConfig, root_key="bot")

engine = create_async_engine(
	bot_config.database_url.get_secret_value(),
	echo=False,
	pool_size=10,
	max_overflow=20
)
async_session = async_sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False
)

@asynccontextmanager
async def get_session() -> AsyncSession:
	async with async_session() as session:
		try:
			yield session
			await session.commit()
		except Exception:
			await session.rollback()
			raise
		finally:
			await session.close()

async def init_db():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
