from aiogram import Router
from aiogram.types import ChatMemberUpdated

from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter

from bot.services.services_container import ServicesContainer

import logging

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))

logger = logging.getLogger(__name__)

def get_event_type(
	old_status: str,
	new_status: str,
	old_is_member: bool | None = None,
	new_is_member: bool | None = None,
	is_adminbot: bool = False
) -> str:
	prefix = "BOT_" if is_adminbot else ""

	def normalize(status: str, is_member: bool | None) -> str:
		if status == "restricted" and is_member is False:
			return "left"
		return status

	old_status = normalize(old_status, old_is_member)
	new_status = normalize(new_status, new_is_member)

	role_map = {
		"member": "USER",
		"administrator": "ADMIN",
		"creator": "CREATOR",
		"restricted": "RESTRICTED",
		"left": "LEFT",
		"kicked": "KICKED",
	}

	old_role = role_map.get(old_status)
	new_role = role_map.get(new_status)

	if not old_role or not new_role:
		return f"{prefix}UNKNOWN"

	return f"{prefix}{old_role}_TO_{new_role}"

@router.chat_member()
async def chat_member(event: ChatMemberUpdated, services: ServicesContainer):
	chat_id = event.chat.id
	user_id = event.new_chat_member.user.id

	await services.telegram_service.invalidate_user_admins_cache(
		chat_id,
		user_id
	)

	username = event.new_chat_member.user.username
	old_status = event.old_chat_member.status
	new_status = event.new_chat_member.status

	role = services.telegram_service.status_to_role_db(
		new_status,
		getattr(event.new_chat_member, "is_member", None)
	)
	
	if new_status == "creator":
		admin_permissions = {"all": True}
		user_permissions = {"all": True}
	else:
		admin_permissions = (
			services.telegram_service.extract_admin_permissions(
				event.new_chat_member
			)
			if new_status in ("administrator", "creator")
			else {}
		)

		user_permissions = (
			services.telegram_service.extract_user_permissions(
				event.new_chat_member
			)
			if new_status not in ("left", "kicked")
			else {}
		)

	await services.members_service.upsert_member(
		chat_id,
		user_id,
		username,
		role,
		user_permissions,
		admin_permissions
	)

	if old_status in ("left", "kicked") and \
	   new_status in ("member", "administrator") or \
	   old_status in ("restricted", "member") and \
	   new_status in ("administrator", "creator"):
		await services.members_service.update_punishments(
			chat_id,
			user_id,
			None, None, None, None
		)
	
	event_type = get_event_type(
		old_status,
		new_status,
		getattr(event.old_chat_member, "is_member", None),
		getattr(event.new_chat_member, "is_member", None),
		False
	)
	logger.info(
		"%s | chat_id=%s user_id=%s",
		event_type,
		chat_id,
		user_id
	)

async def when_bot_added(chat_id: int, services: ServicesContainer):
	admins = await services.telegram_service.get_chat_administrators(chat_id)
	for admin in admins:
		await services.members_service.upsert_member(
			chat_id,
			admin.user.id,
			admin.user.username,
			services.telegram_service.status_to_role_db(admin.status),
			services.telegram_service.extract_user_permissions(admin),
			services.telegram_service.extract_admin_permissions(admin)
		)

	await services.chats_settings_service.upsert_settings(chat_id, None)

@router.my_chat_member()
async def my_chat_member(event: ChatMemberUpdated, services: ServicesContainer):
	chat_id = event.chat.id
	
	await services.telegram_service.invalidate_user_admins_cache(
		chat_id,
		event.new_chat_member.user.id
	)

	new_status = event.new_chat_member.status
	old_status = event.old_chat_member.status
	role = services.telegram_service.status_to_role_db(
		new_status,
		getattr(event.new_chat_member, "is_member", None)
	)

	admin_permissions = (
		services.telegram_service.extract_admin_permissions(
			event.new_chat_member
		)
		if new_status in ("administrator", "creator")
		else {}
	)
	user_permissions = (
		services.telegram_service.extract_user_permissions(
			event.new_chat_member
		)
		if new_status not in ("left", "kicked")
		else {}
	)
		
	await services.bot_chats_info_service.upsert_bot(
		chat_id,
		event.chat.type,
		event.chat.username,
		role,
		user_permissions,
		admin_permissions
	)
	if old_status in ("left", "kicked") and \
	   new_status in ("member", "administrator", "creator"):
		await when_bot_added(chat_id, services)

	event_type = get_event_type(
		old_status,
		new_status,
		getattr(event.old_chat_member, "is_member", None),
		getattr(event.new_chat_member, "is_member", None),
		True
	)
	logger.info(
		"%s | chat_id=%s",
		event_type,
		chat_id
	)
