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

@router.message(Command("ban", "dban", "sban"))
async def ban(message: Message, services: ServicesContainer):
	args = message.text.split()
	target_id, target_username = await services.utils_service.get_id_and_name(
		message,
		args
	)

	delete = message.text.startswith("/dban")
	secret = message.text.startswith("/sban")
	until_time = services.utils_service.get_end_time(args)

	result = await services.bans_service.ban(
		message.chat.id,
		target_id,
		target_username,
		message,
		delete,
		secret,
		until_time
	)

	if delete:
		event_type = "DBAN"
	elif secret:
		event_type = "SBAN"
	else:
		event_type = "BAN"
	logger.info(
		"%s | chat_id=%s user_id=%s target_id=%s",
		event_type,
		message.chat.id,
		message.from_user.id,
		target_id,
	)
	if not secret:
		await message.reply(result)

@router.message(Command("unban"))
async def unban(message: Message, services: ServicesContainer):
	args = message.text.split()
	target_id, target_username = await services.utils_service.get_id_and_name(
		message,
		args
	)

	result = await services.bans_service.unban(
		message.chat.id,
		target_id,
		target_username
	)

	event_type = "UNBAN"
	logger.info(
		"%s | chat_id=%s user_id=%s target_id=%s",
		event_type,
		message.chat.id,
		message.from_user.id,
		target_id,
	)
	await message.reply(result)

@router.message(Command("mute", "dmute", "smute"))
async def mute(message: Message, services: ServicesContainer):
	args = message.text.split()
	target_id, target_username = await services.utils_service.get_id_and_name(
		message,
		args
	)

	delete = message.text.startswith("/dmute")
	secret = message.text.startswith("/smute")
	until_time = services.utils_service.get_end_time(args)

	result = await services.bans_service.mute(
		message.chat.id,
		target_id,
		target_username,
		message,
		delete,
		secret,
		until_time,
	)

	if delete:
		event_type = "DMUTE"
	elif secret:
		event_type = "SMUTE"
	else:
		event_type = "MUTE"
	logger.info(
		"%s | chat_id=%s user_id=%s target_id=%s",
		event_type,
		message.chat.id,
		message.from_user.id,
		target_id,
	)
	if not secret:
		await message.reply(result)

@router.message(Command("unmute"))
async def unmute(message: Message, services: ServicesContainer):
	args = message.text.split()
	target_id, target_username = await services.utils_service.get_id_and_name(
		message,
		args
	)

	result = await services.bans_service.unmute(
		message.chat.id,
		target_id,
		target_username
	)

	event_type = "UNMUTE"
	logger.info(
		"%s | chat_id=%s user_id=%s target_id=%s",
		event_type,
		message.chat.id,
		message.from_user.id,
		target_id,
	)
	await message.reply(result)

@router.message(Command("kick", "dkick", "skick"))
async def kick(message: Message, services: ServicesContainer):
	args = message.text.split()
	target_id, target_username = await services.utils_service.get_id_and_name(
		message,
		args
	)

	delete = message.text.startswith("/dkick")
	secret = message.text.startswith("/skick")

	result = await services.bans_service.kick(
		message.chat.id,
		target_id,
		target_username,
		message,
		delete,
		secret
	)

	if delete:
		event_type = "DKICK"
	elif secret:
		event_type = "SKICK"
	else:
		event_type = "KICK"
	logger.info(
		"%s | chat_id=%s user_id=%s target_id=%s",
		event_type,
		message.chat.id,
		message.from_user.id,
		target_id,
	)
	if not secret:
		await message.reply(result)

@router.message(Command("kickme"), flags={"skip_admin": True})
async def kickme(message: Message, services: ServicesContainer):
	args = message.text.split()
	username = f"@{message.from_user.username}" if message.from_user.username \
												else message.from_user.full_name

	result = await services.bans_service.kickme(
		message.chat.id,
		message.from_user.id,
		username
	)

	event_type = "KICKME"
	logger.info(
		"%s | chat_id=%s user_id=%s",
		event_type,
		message.chat.id,
		message.from_user.id
	)
	await message.reply(result)
