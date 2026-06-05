from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter

from bot.middleware import ErrorMiddleware, AdminMiddleware

from bot.services.services_container import ServicesContainer

import logging

logger = logging.getLogger(__name__)

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
router.message.middleware(ErrorMiddleware())
router.message.middleware(AdminMiddleware())

@router.message(Command("promote", "demote"))
async def promote_demote(message: Message, services: ServicesContainer):
	args = message.text.split()
	user_id, username = await services.utils_service.get_id_and_name(
		message,
		args
	)
	
	is_promote = message.text.startswith("/promote")
	result = await services.admin_service.change_admin_role(
		message.chat.id,
		user_id,
		username,
		is_promote
	)

	action = "promoted" if is_promote else "demoted"
	old_role = "user" if is_promote else "admin"
	new_role = "admin" if is_promote else "user"
	logger.info(
		"in chat %s %s %s was %s to %s",
		message.chat.id,
		old_role,
		user_id,
		action,
		new_role
	)
	
	await message.reply(result)

@router.message(Command("adminlist"))
async def adminlist(message: Message, services: ServicesContainer):
	admins = await services.admin_service.get_chat_administrators(
		message.chat.id
	)
	text = "\n".join(
		f"{a.status} | {a.user.id} | @{a.user.username or 'no_username'}"
		for a in admins
	)
	logger.info(
		"in chat %s admin %s invoked command adminlist",
		message.chat.id,
		message.from_user.id,
	)
	await message.reply("✅ Вот весь список админов чата: \n" + text)

@router.message(Command("anonadmin", "adminerror"))
async def anonadmin_adminerror(message: Message, services: ServicesContainer):
	args = message.text.split()
	
	result = await services.admin_service.chat_settings_switch(
		message.chat.id,
		args
	)
	logger.info(
		"in chat %s admin %s switched setting %s to %s",
		message.chat.id,
		message.from_user.id,
		"anonadmin" if args[0] == "/anonadmin" else "adminerror",
		"on" if args[1] == "on" else "off"
	)

	await message.reply(result)
