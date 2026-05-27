from __future__ import annotations

from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from datetime import datetime, timedelta

class UtilsService:
	def __init__(
		self,
		members_service: MembersService,
		telegram_service: TelegramService
	):
		self.members_service = members_service
		self.telegram_service = telegram_service

	@staticmethod
	def get_end_time(args: list) -> datetime | None:
		if len(args) > 3:
			return None

		if len(args) == 1:
			return datetime(3000, 1, 1)

		if not args[-1].isdigit():
			if len(args) == 2:
				return datetime(3000, 1, 1)
			return None

		seconds = int(args[-1])
		if seconds <= 0:
			return None
		return datetime.utcnow() + timedelta(seconds=seconds)

	async def get_id(self, chat_id: int, target: int | str) -> int | str:
		if target.startswith("@"):
			username = target[1:]
			member = await self.members_service.get_member_by_username(
				chat_id,
				username
			)
			if member is None:
				return "❌ Юзер не найден"
			return member.user_id
		if target.isdigit():
			return int(target)
		return "❌ Некорректный юзернейм/айди"
	
	async def get_id_and_name(self, message: Message, args: list):
		if message.reply_to_message:
			if len(args) > 2:
				return None, "❌ Слишком много аргументов для реплая"
			if len(args) == 2 and not args[1].isdigit:
				return None, "❌ Временной аргумент некорректен"
			user = message.reply_to_message.from_user
			user_id = user.id
			name = f"@{user.username}" if user.username else user.full_name
			return user_id, name

		if len(args) < 2:
			return None, "❌ Отсутствует пользователь"

		user_id = await self.get_id(message.chat.id, args[1])
		if isinstance(user_id, str):
			return None, user_id

		member = await self.telegram_service.get_chat_member(
			message.chat.id,
			user_id
		)
		if not member:
			return None, "❌ Юзер не найден"

		name = f"@{member.user.username}" if member.user.username \
										  else member.user.full_name
		return user_id, name
