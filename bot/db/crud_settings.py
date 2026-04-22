from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ChatSettings

async def upsert_settings(session: AsyncSession, chat_id: int,
							admin: dict | None) -> ChatSettings:
	if admin is None:
		admin = {"anonadmin": False, "adminerror": True}
	chat_settings = await get_settings(session, chat_id)
	if chat_settings:
		chat_settings.admin = admin
	else:
		await update_settings(session, chat_id, admin)
	return chat_settings

async def update_settings(session: AsyncSession, chat_id: int,
							admin: dict | None) -> None:
	chat_settings = ChatSettings(
		chat_id=chat_id,
		admin=admin,
	)
	session.add(chat_settings)

async def get_settings(session: AsyncSession, chat_id: int) -> ChatSettings:
	return await session.get(ChatSettings, chat_id)

async def get_all_settings(session: AsyncSession) -> list[ChatSettings]:
	result = await session.execute(
		select(ChatSettings)
	)
	return result.scalars().all()

async def delete_settings(session: AsyncSession, chat_id: int) -> None:
	await session.execute(
		delete(ChatSettings).where(
			ChatSettings.chat_id == chat_id
		)
	)
