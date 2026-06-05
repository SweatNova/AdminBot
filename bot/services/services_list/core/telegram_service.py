from aiogram import Bot

from aiogram.types import ChatPermissions
from aiogram.types import (
	ChatMemberUnion,
	ChatMemberAdministrator,
	ChatMemberOwner,
	ChatMemberMember,
	ChatMemberRestricted,
	ChatMemberLeft,
	ChatMemberBanned,
)

from datetime import datetime

from bot.storages.redis.cache import (
	get_cache,
	set_cache,
	delete_cache
)

CHAT_MEMBER_TYPES = {
	"ChatMemberAdministrator": ChatMemberAdministrator,
	"ChatMemberOwner": ChatMemberOwner,
	"ChatMemberMember": ChatMemberMember,
	"ChatMemberRestricted": ChatMemberRestricted,
	"ChatMemberLeft": ChatMemberLeft,
	"ChatMemberBanned": ChatMemberBanned,
}

ADMIN_RIGHTS = (
	"can_change_info",
	"can_delete_messages",
	"can_invite_users",
	"can_restrict_members",
	"can_pin_messages",
	"can_promote_members",
	"can_manage_video_chats",
	"can_manage_topics",
	"can_post_stories",
	"can_edit_stories",
	"can_delete_stories",
)
USER_RIGHTS = (
	"can_send_messages",
	"can_send_audios",
	"can_send_documents",
	"can_send_photos",
	"can_send_videos",
	"can_send_video_notes",
	"can_send_voice_notes",
	"can_send_polls",
	"can_send_other_messages",
	"can_add_web_page_previews",
	"can_change_info",
	"can_invite_users",
	"can_pin_messages",
	"can_manage_topics",
)

TELEGRAM_TTL = 60
TELEGRAM_ADMINS_TTL = 300
TELEGRAM_ME_TTL = 3600

class TelegramService:
	def __init__(self, bot: Bot):
		self.bot = bot

	@staticmethod
	def _tg_member_key(chat_id: int, user_id: int) -> str:
		return f"tg_member:{chat_id}:{user_id}"
	@staticmethod
	def _tg_admins_key(chat_id: int) -> str:
		return f"tg_admins:{chat_id}"
	@staticmethod
	def _serialize(tg_member: ChatMemberUnion) -> dict:
		return {
			"_type": tg_member.__class__.__name__,
			"data": tg_member.model_dump(mode="json")
		}
	@staticmethod
	def _deserialize(data: dict) -> ChatMemberUnion:
		cls = CHAT_MEMBER_TYPES[data["_type"]]
		return cls.model_validate(data["data"])

	@staticmethod
	def extract_user_permissions(tg_member) -> dict:
		if tg_member.status == "creator":
			return {"all": True}
		return {
			right: getattr(tg_member, right, True)
			for right in USER_RIGHTS
		}
	@staticmethod
	def extract_admin_permissions(tg_member) -> dict:
		if tg_member.status == "creator":
			return {"all": True}
		return {
			right: getattr(tg_member, right, False)
			for right in ADMIN_RIGHTS
		}
	@staticmethod
	def status_to_role_db(status: str) -> str:
		mapping = {
			"creator": "creator",
			"administrator": "admin",
			"member": "user",
			"kicked": "kicked",
			"left": "left"
		}
		return mapping.get(status, "user")

	async def invalidate_user_admins_cache(
		self,
		chat_id: int,
		user_id: int | None = None
	):
		if user_id is not None:
			await delete_cache(self._tg_member_key(chat_id, user_id))

		await delete_cache(self._tg_admins_key(chat_id))

	async def get_chat_member(
		self,
		chat_id: int,
		user_id: int
	) -> ChatMemberUnion:
		key = self._tg_member_key(chat_id, user_id)
		cached = await get_cache(key)
		if cached:
			return self._deserialize(cached)

		tg_member = await self.bot.get_chat_member(chat_id, user_id)
		await set_cache(key, TELEGRAM_TTL, self._serialize(tg_member))
		return tg_member

	async def get_chat_administrators(
		self,
		chat_id: int
	) -> list[ChatMemberUnion]:
		key = self._tg_admins_key(chat_id)
		cached = await get_cache(key)
		if cached:
			return [self._deserialize(admin) for admin in cached]

		admins = await self.bot.get_chat_administrators(chat_id)
		await set_cache(
			key,
			TELEGRAM_ADMINS_TTL,
			[self._serialize(admin) for admin in admins]
		)
		return admins

	async def promote_chat_member(self, chat_id: int, user_id: int,
								  rights: dict):
		await self.bot.promote_chat_member(
			chat_id=chat_id,
			user_id=user_id,
			**rights
		)
		await delete_cache(self._tg_member_key(chat_id, user_id))
		await delete_cache(self._tg_admins_key(chat_id))

	async def ban_chat_member(self, chat_id: int, user_id: int,
							  until_date: datetime | None = None):
		await self.bot.ban_chat_member(chat_id, user_id, until_date)
		await delete_cache(self._tg_member_key(chat_id, user_id))

	async def unban_chat_member(self, chat_id: int, user_id: int):
		await self.bot.unban_chat_member(chat_id, user_id)
		await delete_cache(self._tg_member_key(chat_id, user_id))

	async def restrict_chat_member(self, chat_id: int, user_id: int,
								   permissions: ChatPermissions,
								   until_date: datetime | None = None):
		await self.bot.restrict_chat_member(
			chat_id=chat_id,
			user_id=user_id,
			permissions=permissions,
			until_date=until_date
		)
		await delete_cache(self._tg_member_key(chat_id, user_id))

	async def delete_message(self, chat_id: int, message_id: int):
		await self.bot.delete_message(chat_id, message_id)
