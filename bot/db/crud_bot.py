from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import BotChatInfo

async def upsert_bot(session: AsyncSession, chat_id: int, chat_type: str,
					 chat_username: str | None, bot_role: str,
					 bot_user_permissions: dict | None,
					 bot_admin_permissions: dict | None):
	bot = await get_bot(session, chat_id)
	if bot:
		bot.chat_type = chat_type
		bot.chat_username = chat_username
		bot.bot_role = bot_role
		bot.bot_user_permissions = bot_user_permissions
		bot.bot_admin_permissions = bot_admin_permissions
	else:
		await update_bot(session, chat_id, chat_type, chat_username, bot_role,
						 bot_user_permissions, bot_admin_permissions)
	return bot

async def update_bot(session: AsyncSession, chat_id: int, chat_type: str,
					 chat_username: str | None, bot_role: str,
					 bot_user_permissions: dict | None,
					 bot_admin_permissions: dict | None) -> None:
	bot = BotChatInfo(
		chat_id=chat_id,
		chat_type=chat_type,
		chat_username=chat_username,
		bot_role=bot_role,
		bot_user_permissions=bot_user_permissions,
		bot_admin_permissions=bot_admin_permissions,
	)
	session.add(bot)

async def get_bot(session: AsyncSession, chat_id: int):
	return await session.get(BotChatInfo, chat_id)

async def get_bots(session: AsyncSession):
	result = await session.execute(
		select(BotChatInfo)
	)
	return result.scalars().all()

async def get_bot_by_chat_username(session: AsyncSession, chat_username: str):
	result = await session.execute(
		select(BotChatInfo).where(
			BotChatInfo.chat_username == chat_username
		)
	)
	return result.scalar_one_or_none()

async def delete_bot(session: AsyncSession, chat_id: int):
	await session.execute(
		delete(BotChatInfo).where(
			BotChatInfo.chat_id == chat_id
		)
	)
