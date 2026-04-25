from aiogram import Router, Bot
from aiogram.types import ChatMemberUpdated

from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter

from bot.db import get_session
from bot.db.crud import upsert_member
from bot.db.crud_bot import upsert_bot
from bot.db.crud_settings import get_settings, upsert_settings
from bot.utils import (
	status_to_db,
	extract_admin_permissions,
	extract_user_permissions
)

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))

@router.chat_member()
async def members_update(event: ChatMemberUpdated):
	chat_id = event.chat.id
	user_id = event.new_chat_member.user.id
	username = event.new_chat_member.user.username
	status = event.new_chat_member.status
	role = status_to_db(status)

	if status in ("administrator", "creator"):
		admin_permissions = extract_admin_permissions(event.new_chat_member)
	else:
		admin_permissions = {}
	if status not in ("left", "kicked"):
		user_permissions = extract_user_permissions(event.new_chat_member)
	else:
		user_permissions = {}

	async with get_session() as session:
		await upsert_member(session, chat_id, user_id, username,
							role, user_permissions, admin_permissions)

async def when_bot_added(session, bot: Bot, chat_id: int):
	admins = await bot.get_chat_administrators(chat_id)
	for admin in admins:
		await upsert_member(
			session,
			chat_id,
			admin.user.id,
			admin.user.username,
			status_to_db(admin.status),
			extract_user_permissions(admin),
			extract_admin_permissions(admin)
		)
	chat_settings = await get_settings(session, chat_id)
	if not chat_settings:
		await upsert_settings(session, chat_id, None)

@router.my_chat_member()
async def my_members_update(event: ChatMemberUpdated, bot: Bot):
	chat_id = event.chat.id
	chat_type = event.chat.type
	chat_username = event.chat.username
	new_status = event.new_chat_member.status
	old_status = event.old_chat_member.status
	bot_role = status_to_db(new_status)

	if new_status in ("administrator", "creator"):
		admin_permissions = extract_admin_permissions(event.new_chat_member)
	else:
		admin_permissions = {}
	if new_status not in ("left", "kicked"):
		user_permissions = extract_user_permissions(event.new_chat_member)
	else:
		user_permissions = {}

	async with get_session() as session:
		await upsert_bot(session, chat_id, chat_type, chat_username,
						 bot_role, user_permissions, admin_permissions)
		if old_status in ("left", "kicked") and \
		   new_status in ("member", "administrator", "creator"):
			await when_bot_added(session, bot, chat_id)
