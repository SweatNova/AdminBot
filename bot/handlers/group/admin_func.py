from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter

from bot.middleware import ErrorMiddleware, AdminMiddleware

from bot.services.services_container import ServicesContainer

import time

import logging

logger = logging.getLogger(__name__)

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
router.message.middleware(ErrorMiddleware())
router.message.middleware(AdminMiddleware())

@router.message(Command("promote", "demote"))
async def promote_demote(
	message: Message,
	services: ServicesContainer,
	request_start: float
):
	args = message.text.split()
	target_id, target_username = await services.utils_service.get_id_and_name(
		message,
		args
	)
	
	is_promote = message.text.startswith("/promote")
	result = await services.admin_service.change_admin_role(
		message.chat.id,
		target_id,
		target_username,
		is_promote
	)

	event_type = "PROMOTE" if is_promote else "DEMOTE"
	response_time = round((time.perf_counter() - request_start) * 1000, 2)
	logger.info(
		"%s | chat_id=%s admin_id=%s target_id=%s response_time=%sms",
		event_type,
		message.chat.id,
		message.from_user.id,
		target_id,
		response_time
	)
	await message.reply(result)

@router.message(Command("adminlist"))
async def adminlist(
	message: Message,
	services: ServicesContainer,
	request_start: float
):
	admins = await services.admin_service.get_chat_administrators(
		message.chat.id
	)
	text = "\n".join(
		f"{a.status} | {a.user.id} | @{a.user.username or 'no_username'}"
		for a in admins
	)

	event_type = "ADMINLIST"
	response_time = round((time.perf_counter() - request_start) * 1000, 2)
	logger.info(
		"%s | chat_id=%s admin_id=%s response_time=%sms",
		event_type,
		message.chat.id,
		message.from_user.id,
		response_time
	)
	await message.reply(
		"✅ Here is the full list of chat administrators: \n" + text
	)

@router.message(Command("anonadmin", "adminerror"))
async def anonadmin_adminerror(
	message: Message,
	services: ServicesContainer,
	request_start: float
):
	args = message.text.split()
	
	result = await services.admin_service.chat_settings_switch(
		message.chat.id,
		args
	)

	event_type = "ANONADMIN" if args[0] == "/anonadmin" else "ADMINERROR"
	response_time = round((time.perf_counter() - request_start) * 1000, 2)
	logger.info(
		"%s | chat_id=%s user_id=%s response_time=%sms",
		event_type,
		message.chat.id,
		message.from_user.id,
		response_time
	)
	await message.reply(result)
