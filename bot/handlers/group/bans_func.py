from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter
from aiogram.exceptions import TelegramBadRequest

from datetime import datetime, timedelta

from bot.db import get_session
from bot.db.crud_members import upsert_member, upsert_punishments
from bot.utils import is_admin, get_id
from bot.middleware import AdminMiddleware

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
router.message.middleware(AdminMiddleware())

@router.message(F.text == "/kickme", flags={"skip_admin": True})
async def kick_me(message: Message, bot: Bot):
	user_id = message.from_user.id
	chat_id = message.chat.id
	
	await message.bot.ban_chat_member(chat_id, user_id)
	await message.bot.unban_chat_member(chat_id, user_id)

	username = message.from_user.username
	if username:
		text = f"@{username}"
	else:
		text = message.from_user.full_name
	await message.reply(f"Пользователь {text} сам вышел из чата")

@router.message(F.text.startswith("/ban"))
async def ban(message: Message, bot: Bot):
	args = message.text.split()
	if len(args) < 2 or len(args) > 3:
		return await message.reply("Некорректный вызов команды")
	if len(args) == 3:
		try:
			duration = int(args[2])
		except ValueError:
			return await message.reply("Временной аргумент некорректен")
		if duration <= 0:
			return await message.reply("Время должно быть больше 0")
		end_time = datetime.utcnow() + timedelta(seconds=duration)
	else:
		end_time = datetime.max

	async with get_session() as session:
		user_id = await get_id(session, message.chat.id, args[1])
		if isinstance(user_id, str):
			return await message.reply(user_id)

		member = await bot.get_chat_member(message.chat.id, user_id)
		if not member:
			return await message.reply("❌ Юзер не в чате")
		if member.user.username:
			text = f"@{member.user.username}"
		else:
			text = member.full_name

		try:
			if await is_admin(bot, message.chat.id, user_id):
				return await message.reply("❌ Нельзя банить админов")
			await message.bot.ban_chat_member(message.chat.id, user_id)
			await upsert_punishments(session, message.chat.id, user_id,
									 "banned", message.from_user.username,
									 datetime.utcnow(), end_time)
		except TelegramBadRequest as e:
			return await message.reply(f"❌ Ошибка telegram: {e}")
	await message.reply(f"Пользователь {text} был забанен")
