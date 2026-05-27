from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Any, Awaitable

from bot.services.services_container import ServicesContainer

class AdminMiddleware(BaseMiddleware):
	async def __call__(
		self,
		handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
		event: Message,
		data: dict[str, Any]
	) -> Any:
		services: ServicesContainer = data["services"]
		handler_object = data.get("handler")
		flags = getattr(handler_object, "flags", {})
		if flags.get("skip_admin"):
			return await handler(event, data)

		chat_id = event.chat.id
		user_id = event.from_user.id

		chat_settings = await services.chats_settings_service.get_settings(
			chat_id
		)
		adminerror = chat_settings.admin["adminerror"]

		if not await services.telegram_service.is_admin(chat_id, user_id):
			if adminerror:
				await event.reply("❌ У вас недостаточно прав")
				return
			return

		bot = await services.telegram_service.get_chat_member(
			chat_id,
			data["bot"].id
		)
		if bot.status not in ("administrator", "creator"):
			if adminerror:
				await event.reply("❌ У бота нет прав администратора")
				return
			return
		return await handler(event, data)
