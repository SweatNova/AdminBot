from aiogram.types import Message, User
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ChatPermissions

from bot.db import get_session
from bot.db.crud_members import get_member_by_username, upsert_punishments
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
	args = message.text.lower().split()
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

async def apply_punishments(session, bot, message, user_id, username,
							command: str, end_time):
	try:
		chat_id = message.chat.id
		if await is_admin(bot, chat_id, user_id):
			return "❌ Нельзя ограничивать админов"
		if message.text.startswith(("/dban", "/dmute", "/dkick")) and \
		   message.reply_to_message:
			await bot.delete_message(chat_id,
									 message.reply_to_message.message_id)
		if message.text.startswith(("/sban", "/smute", "/skick")):
			await message.delete()

		if "ban" in command:
			await bot.ban_chat_member(chat_id, user_id)
			action = "забанен"
		elif "mute" in command:
			await bot.restrict_chat_member(
				chat_id=chat_id,
				user_id=user_id,
				permissions=ChatPermissions(
					can_send_messages=False
				)
			)
			action = "замучен"
		elif "kick" in command:
			await bot.ban_chat_member(chat_id, user_id)
			await bot.unban_chat_member(chat_id, user_id)
			action = "кикнут"
		
		status = "banned" if "ban" in command else "muted"

		if not "kick" in command:
			await upsert_punishments(
				session,
				chat_id,
				user_id,
				status,
				message.from_user.username,
				datetime.utcnow(),
				end_time
			)
		return f"Пользователь {username} был {action}"
	except TelegramBadRequest as e:
		return f"❌ Ошибка telegram: {e}"

async def remove_punishments(session, bot, message, user_id, username,
							 command: str):
	try:
		chat_id = message.chat.id
		if await is_admin(bot, chat_id, user_id):
			return "❌ Нельзя убирать ограничения админов"

		if command == "/unban":
			await bot.unban_chat_member(chat_id, user_id)
			action = "разбанен"
		elif command == "/unmute":
			await bot.restrict_chat_member(
				chat_id=chat_id,
				user_id=user_id,
				permissions=ChatPermissions(
					can_send_messages=True,
				)
			)
			action = "размучен"
		await upsert_punishments(
			session,
			chat_id,
			user_id,
			None, None, None, None
		)
		return f"Пользователь {username} был {action}"
	except TelegramBadRequest as e:
		return f"❌ Ошибка telegram: {e}"
