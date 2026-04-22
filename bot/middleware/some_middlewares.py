from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Any, Awaitable
from bot.utils import is_admin
from bot.db import get_session
from bot.db.crud_settings import upsert_settings, get_settings

class AdminMiddleware(BaseMiddleware):
	async def __call__(
		self,
		handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
		event: Message,
		data: dict[str, Any]
	) -> Any:
		handler_object = data.get("handler")
		flags = getattr(handler_object, "flags", {})
		if flags.get("skip_admin"):
			return await handler(event, data)

		async with get_session() as session:
			chat_id = event.chat.id
			chat_settings = await get_settings(session, event.chat.id)
			adminerror = chat_settings.admin["adminerror"]
			
		if not await is_admin(event):
			if adminerror:
				await event.reply("❌ У вас недостаточно прав")
				return
			return
		bot = data["bot"]
		_bot_ = await bot.get_chat_member(event.chat.id, bot.id)
		if _bot_.status not in ("administrator", "creator"):
			if adminerror:
				await event.reply("❌ У бота нет прав администратора")
				return
			return
		return await handler(event, data)

class ChatsSettingsMiddleware(BaseMiddleware):
	async def __call__(
		self,
		handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
		event: Message,
		data: dict[str, Any]
	) -> Any:
		chat_id = event.chat.id
		async with get_session() as session:
			chat_settings = await get_settings(session, chat_id)
			if chat_settings:
				return await handler(event, data)
			await upsert_settings(session, chat_id, None)

