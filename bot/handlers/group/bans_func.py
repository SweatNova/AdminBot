from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter
from aiogram.exceptions import TelegramBadRequest

from bot.storages.postgre import get_session
from bot.utils import (
	is_admin,
	get_id_and_name,
	get_end_time,
	apply_punishments,
	remove_punishments	
)
from bot.middleware import AdminMiddleware

from datetime import datetime

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
router.message.middleware(AdminMiddleware())

@router.message(F.text == "/kickme", flags={"skip_admin": True})
async def kickme(message: Message, bot: Bot):
	args = message.text.split()
	if len(args) > 1:
		return await message.reply("Команда не требует аргументов")
	if await is_admin(bot, message.chat.id, message.from_user.id):
		return await message.reply("Вы админ! лишите себя прав "
								   "для вызова команды")
	await bot.ban_chat_member(message.chat.id, message.from_user.id)
	await bot.unban_chat_member(message.chat.id, message.from_user.id)	
	await message.reply(f"Пользователь @{message.from_user.username} "
						"самовыпилился из чата")

@router.message(F.text.startswith((
    "/ban", "/dban", "/sban",
    "/mute", "/dmute", "/smute",
    "/kick", "/dkick", "/skick"
)))
async def ban_mute_kick(message: Message, bot: Bot):
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
			command=args[0],
			end_time=get_end_time(args)
		)
		if not args[0] in ("/sban", "/smute", "/skick"):
			await message.reply(result)

@router.message(F.text.startswith(("/unban", "/unmute")))
async def unban_unmute(message: Message, bot: Bot):
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
			command=args[0]
		)
	await message.reply(result)
