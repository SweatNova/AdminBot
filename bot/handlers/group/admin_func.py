from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter
from aiogram.exceptions import TelegramBadRequest

from bot.storages.postgre import get_session
from bot.utils import (
	extract_admin_permissions,
	get_id,
	chat_settings_switch,
	change_role
)
from bot.middleware import AdminMiddleware

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
router.message.middleware(AdminMiddleware())

@router.message(F.text.startswith(("/promote", "/demote")))
async def promote_demote_user(message: Message, bot: Bot):
	args = message.text.split()
	if len(args) < 2:
		return await message.reply("Введите айди или юзернейм")
	if len(args) > 2:
		return await message.reply("Не должно быть никаких аргументов "
								   "кроме юзернейма")

	async with get_session() as session:
		result = await change_role(
			bot=bot,
			session=session,
			chat_id=message.chat.id,
			command=args[0],
			target=args[1]
		)
	await message.reply(result)

@router.message(F.text == "/adminlist")
async def admin_list(message: Message, bot: Bot):
	admins = await bot.get_chat_administrators(message.chat.id)
	text = "\n".join(
		f"{a.status} | {a.user.id} | @{a.user.username or 'no_username'}"
		for a in admins
	)
	await message.reply("✅ Вот весь список админов чата: \n" + text)

@router.message(F.text.startswith("/anonadmin"))
async def anon_admin(message: Message, bot: Bot):
	await chat_settings_switch(message, bot, "admin")
@router.message(F.text.startswith("/adminerror"))
async def admin_error(message: Message, bot: Bot):
	await chat_settings_switch(message, bot, "admin")
