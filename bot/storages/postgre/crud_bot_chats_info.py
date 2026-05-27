from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import BotChatInfo

async def get_bot_crud(session: AsyncSession, chat_id: int) -> BotChatInfo:
	return await session.get(BotChatInfo, chat_id)

async def get_bots_crud(session: AsyncSession) -> list[BotChatInfo]:
	result = await session.execute(
		select(BotChatInfo)
	)
	return result.scalars().all()

async def create_bot_crud(session: AsyncSession, chat_id: int, chat_type: str,
					 	  chat_username: str | None, bot_role: str,
					 	  bot_user_permissions: dict | None,
					 	  bot_admin_permissions: dict | None) -> BotChatInfo:
	bot = BotChatInfo(
		chat_id=chat_id,
		chat_type=chat_type,
		chat_username=chat_username,
		bot_role=bot_role,
		bot_user_permissions=bot_user_permissions,
		bot_admin_permissions=bot_admin_permissions,
	)
	session.add(bot)
	return bot

async def delete_bot_crud(session: AsyncSession, chat_id: int):
	await session.execute(
		delete(BotChatInfo).where(
			BotChatInfo.chat_id == chat_id
		)
	)
