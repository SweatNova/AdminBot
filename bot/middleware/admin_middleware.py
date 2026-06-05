from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Any, Awaitable

from bot.services.services_container import ServicesContainer

from bot.exceptions import UserHasNoRightsError, AdminBotHasNoRightsError

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
		data["adminerror"] = chat_settings.admin["adminerror"]

		member = await services.members_service.get_member(chat_id, user_id)
		if member.role not in ("creator", "admin"):
			raise UserHasNoRightsError

		bot = await services.bot_chats_info_service.get_bot(chat_id)
		if bot.bot_role not in ("creator", "admin"):
			raise AdminBotHasNoRightsError
		return await handler(event, data)
