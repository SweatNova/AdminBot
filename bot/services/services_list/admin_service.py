from __future__ import annotations

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ChatPermissions
from aiogram.types import ChatAdministratorRights

class AdminService:
	def __init__(
		self,
		members_service: MembersService,
		chats_settings_service: ChatsSettingsService,
		telegram_service: TelegramService,
	):
		self.members_service = members_service
		self.chats_settings_service = chats_settings_service
		self.telegram_service = telegram_service

	async def change_admin_role(self, chat_id: int, user_id: int,
								username: str, is_promote: bool) -> str:
		rights = {
			"can_change_info": is_promote,
			"can_delete_messages": is_promote,
			"can_invite_users": is_promote,
			"can_restrict_members": is_promote,
			"can_pin_messages": is_promote,
			"can_promote_members": is_promote
		}
		try:
			telegram_member = await self.telegram_service.get_chat_member(
				chat_id,
				user_id
			)
			if telegram_member.user.is_bot:
				return "❌ Нельзя менять права у ботов"
		except TelegramBadRequest as e:
			if "PARTICIPANT_ID_INVALID" in str(e):
				return "❌ Некорректный айди пользователя"

		role = "admin" if is_promote else "user"
		action = "повышен" if is_promote else "понижен"

		try:
			await self.telegram_service.promote_chat_member(
				chat_id,
				user_id,
				rights
			)
			return f"✅ Пользователь {username} {action} до {role}"
		except TelegramBadRequest as e:
			if "CHAT_ADMIN_REQUIRED" in str(e):
				return f"❌ Админ был назначен не ботом"
			else:
				return f"❌ Ошибка telegram: {e}"

	async def get_chat_administrators(self, chat_id: int) -> list[dict]:
		return await self.telegram_service.get_chat_administrators(chat_id)

	async def chat_settings_switch(self, chat_id: int, args: list) -> str:
		return await self.chats_settings_service.chat_settings_switch(
			chat_id,
			args,
			"admin"
		)
