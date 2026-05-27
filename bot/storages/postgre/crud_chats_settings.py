from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ChatSettings

async def get_settings_crud(session: AsyncSession,
							chat_id: int) -> ChatSettings:
	return await session.get(ChatSettings, chat_id)

async def get_all_settings_crud(session: AsyncSession) -> list[ChatSettings]:
	result = await session.execute(
		select(ChatSettings)
	)
	return result.scalars().all()

async def create_settings_crud(session: AsyncSession, chat_id: int,
						  	   admin: dict | None) -> ChatSettings:
	if admin is None:
		admin = {"anonadmin": False, "adminerror": True}
	chat_settings = ChatSettings(
		chat_id=chat_id,
		admin=admin
	)
	session.add(chat_settings)
	return chat_settings

async def delete_settings_crud(session: AsyncSession, chat_id: int) -> None:
	await session.execute(
		delete(ChatSettings).where(
			ChatSettings.chat_id == chat_id
		)
	)
