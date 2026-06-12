from __future__ import annotations

from aiogram.exceptions import TelegramBadRequest
from bot.exceptions import (
	CantChangeBotsRightsError,
	CantModerateAssignedNotByBotAdminsError,
	AdminBotHasNoRightsError
)

class AdminService:
	def __init__(
		self,
		members_service: MembersService,
		bot_chats_info_service: BotChatsInfoService,
		chats_settings_service: ChatsSettingsService,
		telegram_service: TelegramService,
	):
		self.members_service = members_service
		self.bot_chats_info_service = bot_chats_info_service
		self.chats_settings_service = chats_settings_service
		self.telegram_service = telegram_service

	async def change_admin_role(
		self,
		chat_id: int,
		user_id: int,
		username: str,
		is_promote: bool
	) -> str:
		rights = {
			"can_change_info": is_promote,
			"can_delete_messages": is_promote,
			"can_invite_users": is_promote,
			"can_restrict_members": is_promote,
			"can_pin_messages": is_promote,
			"can_promote_members": is_promote
		}
		bot = await self.bot_chats_info_service.get_bot(chat_id)
		if not bot.bot_admin_permissions["can_promote_members"]:
			raise AdminBotHasNoRightsError

		missing_rights = [
			right
			for right, required in rights.items()
			if required and not bot.bot_admin_permissions.get(right, False)
		]
		if missing_rights:
			raise AdminBotHasNoRightsError

		member = await self.members_service.get_member(
			chat_id,
			user_id
		)
		if member.username.lower().endswith("bot"):
			raise CantChangeBotsRightsError

		role = "admin" if is_promote else "user"
		action = "promoted" if is_promote else "demoted"

		try:
			await self.telegram_service.promote_chat_member(
				chat_id,
				user_id,
				rights
			)
		except TelegramBadRequest as t_e:
			if "CHAT_ADMIN_REQUIRED" in str(t_e):
				raise CantModerateAssignedNotByBotAdminsError(user_id)

		return f"✅ User {username} {action} to {role}"

	async def get_chat_administrators(self, chat_id: int) -> list[dict]:
		return await self.telegram_service.get_chat_administrators(chat_id)

	async def chat_settings_switch(self, chat_id: int, args: list) -> str:
		return await self.chats_settings_service.chat_settings_switch(
			chat_id,
			args,
			"admin"
		)
