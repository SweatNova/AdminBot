from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter

from bot.middleware import AdminMiddleware

from bot.services.services_container import ServicesContainer

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
router.message.middleware(AdminMiddleware())

@router.message(Command("promote", "demote"))
async def promote_demote(message: Message, services: ServicesContainer):
	args = message.text.split()
	if len(args) > 2:
		return await message.reply(
			"❌ Не должно быть никаких аргументов кроме юзернейма или айди"
		)

	user_id, username = await services.utils_service.get_id_and_name(
		message,
		args
	)
	if user_id is None:
		return await message.reply(username)
	
	is_promote = message.text.startswith("/promote")
	result = await services.admin_service.change_admin_role(
		message.chat.id,
		user_id,
		username,
		is_promote
	)
	await message.reply(result)

@router.message(Command("adminlist"))
async def adminlist(message: Message, services: ServicesContainer):
	try:
		admins = await services.admin_service.get_chat_administrators(
			message.chat.id
		)
	except Exception as e:
		return await message.reply(e)

	text = "\n".join(
		f"{a.status} | {a.user.id} | @{a.user.username or 'no_username'}"
		for a in admins
	)
	await message.reply("✅ Вот весь список админов чата: \n" + text)

@router.message(Command("anonadmin", "adminerror"))
async def anonadmin_adminerror(message: Message, services: ServicesContainer):
	args = message.text.split()
	if len(args) < 2:
		return await message.reply("❌ Введите новое значение настройки")
	if len(args) > 2:
		return await message.reply("❌ Слишком много аргументов")

	result = await services.admin_service.chat_settings_switch(
		message.chat.id,
		args
	)
	await message.reply(result)
