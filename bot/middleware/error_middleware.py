from aiogram import BaseMiddleware

from aiogram.exceptions import TelegramBadRequest

from bot.exceptions import BotError

import time

import logging

logger = logging.getLogger(__name__)

class ErrorMiddleware(BaseMiddleware):
	async def __call__(self, handler, event, data):
		try:
			return await handler(event, data)

		except BotError as e:
			response_time = round(
				(time.perf_counter() - data["request_start"]) * 1000,
				2
			)

			logger.warning(
				"%s response_time=%sms",
				e.log(event),
				response_time
			)

			await event.reply(str(e))
