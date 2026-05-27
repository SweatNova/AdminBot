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

@router.message(Command("ban", "dban", "sban"))
async def ban(message: Message, services: ServicesContainer):
	args = message.text.split()
	if len(args) > 3:
		return await message.reply("❌ Слишком много аргументов")

	user_id, username = await services.utils_service.get_id_and_name(
		message,
		args
	)
	if user_id is None:
		return await message.reply(username)

	delete = message.text.startswith("/dban")
	secret = message.text.startswith("/sban")
	until_time = services.utils_service.get_end_time(args)
	if until_time is None:
		return await message.reply("❌ Некорректный временной аргумент")

	result = await services.bans_service.ban(
		message.chat.id,
		user_id,
		username,
		message,
		delete,
		secret,
		until_time
	)
	if not secret:
		await message.reply(result)

@router.message(Command("unban"))
async def unban(message: Message, services: ServicesContainer):
	args = message.text.split()
	if len(args) > 2:
		return await message.reply("❌ Слишком много аргументов")

	user_id, username = await services.utils_service.get_id_and_name(
		message,
		args
	)
	if user_id is None:
		return await message.reply(username)

	result = await services.bans_service.unban(
		message.chat.id,
		user_id,
		username
	)
	await message.reply(result)

@router.message(Command("mute", "dmute", "smute"))
async def mute(message: Message, services: ServicesContainer):
	args = message.text.split()
	if len(args) > 3:
		return await message.reply("❌ Слишком много аргументов")

	user_id, username = await services.utils_service.get_id_and_name(
		message,
		args
	)
	if user_id is None:
		return await message.reply(username)

	delete = message.text.startswith("/dmute")
	secret = message.text.startswith("/smute")
	until_time = services.utils_service.get_end_time(args)
	if until_time is None:
		return await message.repl("❌ Некорректный временной аргумент")

	result = await services.bans_service.mute(
		message.chat.id,
		user_id,
		username,
		message,
		delete,
		secret,
		until_time,
	)
	if not secret:
		await message.reply(result)

@router.message(Command("unmute"))
async def unmute(message: Message, services: ServicesContainer):
	args = message.text.split()
	if len(args) > 2:
		return await message.reply("❌ Слишком много аргументов")

	user_id, username = await services.utils_service.get_id_and_name(
		message,
		args
	)
	if user_id is None:
		return await message.reply(username)

	result = await services.bans_service.unmute(
		message.chat.id,
		user_id,
		username
	)
	await message.reply(result)

@router.message(Command("kick", "dkick", "skick"))
async def kick(message: Message, services: ServicesContainer):
	args = message.text.split()
	if len(args) > 2:
		return await message.reply("❌ Слишком много аргументов")

	user_id, username = await services.utils_service.get_id_and_name(
		message,
		args
	)
	if user_id is None:
		return await message.reply(username)

	delete = message.text.startswith("/dkick")
	secret = message.text.startswith("/skick")

	result = await services.bans_service.kick(
		message.chat.id,
		user_id,
		username,
		message,
		delete,
		secret,
	)
	if not secret:
		await message.reply(result)

@router.message(Command("kickme"), flags={"skip_admin": True})
async def kickme(message: Message, services: ServicesContainer):
	args = message.text.split()
	if len(args) > 1:
		return await message.reply("❌ Команда не требует аргументов")

	user_id = message.from_user.id
	username = f"@{message.from_user.username}" if message.from_user.username \
												else message.from_user.full_name

	result = await services.bans_service.kickme(
		message.chat.id,
		user_id,
		username
	)
	await message.reply(result)
