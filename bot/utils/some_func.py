from aiogram.types import Message, User
from aiogram import Bot
from bot.db import get_session
from bot.db.crud_members import get_member_by_username
from bot.db.crud_settings import get_settings, upsert_settings, delete_settings

from datetime import datetime, timedelta

async def is_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
	member = await bot.get_chat_member(
		chat_id=chat_id,
		user_id=user_id
	)
	return member.status in ("administrator", "creator")

def status_to_db(status: str) -> str:
	mapping = {
		"creator": "creator",
        "administrator": "admin",
		"member": "user",
		"kicked": "kicked",
		"left": "left"
	}
	return mapping.get(status, "user")

def extract_admin_permissions(tg_member) -> dict:
	if tg_member.status == "creator":
		return {
			"all": True
		}
	return {
		"can_change_info": getattr(tg_member,
							"can_change_info", False),
		"can_delete_messages": getattr(tg_member,
							"can_delete_messages", False),
		"can_invite_users": getattr(tg_member,
							"can_invite_users", False),
		"can_restrict_members": getattr(tg_member,
							"can_restrict_members", False),
		"can_pin_messages": getattr(tg_member,
							"can_pin_messages", False),
		"can_promote_members": getattr(tg_member,
							"can_promote_members", False),
		"can_manage_video_chats": getattr(tg_member,
							"can_manage_video_chats", False),
		"can_manage_topics": getattr(tg_member,
							"can_manage_topics", False)
    }
def extract_user_permissions(tg_member) -> dict:
    return {
		"can_send_messages": getattr(tg_member,
							"can_send_messages", True),
		"can_send_media_messages": getattr(tg_member,
							"can_send_media_messages", True),
		"can_send_audios": getattr(tg_member,
							"can_send_audios", True),
		"can_send_voice_notes": getattr(tg_member,
							"can_send_voice_notes", True),
		"can_send_video_notes": getattr(tg_member,
							"can_send_video_notes", True),
		"can_send_polls": getattr(tg_member,
							"can_send_polls", True),
		"can_add_web_page_previews": getattr(tg_member,
							"can_add_web_page_previews", True),
		"can_invite_users": getattr(tg_member,
							"can_invite_users", True),
		"can_pin_messages": getattr(tg_member,
							"can_pin_messages", True),
		"can_change_info": getattr(tg_member,
							"can_change_info", True)
	}

async def get_id(session, chat_id, target):
	if target.startswith("@"):
		member = await get_member_by_username(
			session=session,
			chat_id=chat_id,
			username=target[1:]
		)
		if not member:
			return "❌ Пользователь не найден"
		return member.user_id
	elif target.isdigit():
		return int(target)
	return "❌ Некорректный формат"

async def chat_settings_switch(message: Message, bot: Bot, chat_arg: str):
	args = message.text.lower().split(maxsplit=1)
	if len(args) != 2:
		return await message.reply("Выберите режим on/off")
	if not args[1] in ["on", "off"]:
		return await message.reply("❌ Неизвестный режим")

	async with get_session() as session:
		chat_settings = await get_settings(session, message.chat.id)
		value = getattr(chat_settings, chat_arg, None)
		chat_dict = dict(value)
		setting = args[0][1:]
		if args[1] == "on":
			chat_dict[setting] = True
		else:
			chat_dict[setting] = False
		await upsert_settings(session, message.chat.id, chat_dict)
	await message.reply(f"✅ Настройка {args[0]} переключена")

async def get_id_and_name(session, bot: Bot, message: Message, args: list):
	if message.reply_to_message:
		user = message.reply_to_message.from_user
		user_id = user.id
		name = f"@{user.username}" if user.username else user.full_name
		return user_id, name

	if len(args) < 2:
		return None, "Отсутствует пользователь"

	user_id = await get_id(session, message.chat.id, args[1])
	if isinstance(user_id, str):
		return None, user_id

	member = await bot.get_chat_member(message.chat.id, user_id)
	if not member:
		return None, "❌ Юзер не в чате"

	name = f"@{member.user.username}" if member.user.username \
									  else member.full_name
	return user_id, name

def get_end_time(args: list) -> datetime:
	if len(args) >= 2 and args[-1].isdigit():
		duration = int(args[-1])
		if duration <= 0:
			return None
		return datetime.utcnow() + timedelta(seconds=duration)
	return datetime.max
