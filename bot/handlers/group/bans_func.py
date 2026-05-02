from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter
from aiogram.types import ChatPermissions
from aiogram.exceptions import TelegramBadRequest

from bot.db import get_session
from bot.db.crud_members import upsert_punishments
from bot.utils import is_admin, get_id, get_id_and_name, get_end_time
from bot.middleware import AdminMiddleware

from datetime import datetime

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
router.message.middleware(AdminMiddleware())

async def apply_punishments(session, bot, message, user_id, username,
							command: str, end_time):
	try:
		chat_id = message.chat.id
		if await is_admin(bot, chat_id, user_id):
			return await message.reply("❌ Нельзя ограничивать админов")
		if message.text.startswith("/dban") or \
		   message.text.startswith("/dmute") and \
		   message.reply_to_message:
			await bot.delete_message(chat_id,
									 message.reply_to_message.message_id)
		if message.text.startswith("/sban") or \
		   message.text.startswith("/smute"):
			await message.delete()

		if command == "ban":
			await bot.ban_chat_member(chat_id, user_id)
			action = "забанен"
		elif command == "mute":
			await bot.restrict_chat_member(
				chat_id=chat_id,
				user_id=user_id,
				permissions=ChatPermissions(
					can_send_messages=False
				)
			)
			action = "замучен"
		await upsert_punishments(
			session,
			chat_id,
			user_id,
			command,
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
			return await message.reply("❌ Админов нельзя ограничивать")

		if command == "unban":
			await bot.unban_chat_member(chat_id, user_id)
			action = "разбанен"
		elif command == "unmute":
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

@router.message(F.text.startswith("/ban") |
				F.text.startswith("/dban") |
				F.text.startswith("/sban"))
async def ban(message: Message, bot: Bot):
	args = message.text.split()
	async with get_session() as session:
		user_id, username = await get_id_and_name(session, bot, message, args)
		if user_id is None:
			return await message.reply(username)

		result = await apply_punishments(
			session,
			bot,
			message,
			user_id,
			username,
			command="ban",
			end_time=get_end_time(args)
		)
		if args[0] != "/sban":
			await message.reply(result)

@router.message(F.text.startswith("/unban"))
async def unban_handler(message: Message, bot: Bot):
	args = message.text.split()
	async with get_session() as session:
		user_id, username = await get_id_and_name(session, bot, message, args)
		if user_id is None:
			return await message.reply(username)

		result = await remove_punishments(
			session,
			bot,
			message,
			user_id,
			username,
			command="unban"
		)
	await message.reply(result)

@router.message(F.text.startswith("/mute") |
				F.text.startswith("/dmute") |
				F.text.startswith("/smute"))
async def mute(message: Message, bot: Bot):
	args = message.text.split()
	async with get_session() as session:
		user_id, username = await get_id_and_name(session, bot, message, args)
		if user_id is None:
			return await message.reply(username)

		result = await apply_punishments(
			session,
			bot,
			message,
			user_id,
			username,
			command="mute",
			end_time=get_end_time(args)
		)
		if args[0] != "/smute":
			await message.reply(result)

@router.message(F.text.startswith("/unmute"))
async def unmute_handler(message: Message, bot: Bot):
	args = message.text.split()
	async with get_session() as session:
		user_id, username = await get_id_and_name(session, bot, message, args)
		if user_id is None:
			return await message.reply(username)

		result = await remove_punishments(
			session,
			bot,
			message,
			user_id,
			username,
			command="unmute",
		)
	await message.reply(result)

