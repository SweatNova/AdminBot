from aiogram import BaseMiddleware

from aiogram.exceptions import TelegramBadRequest

from bot.exceptions import BotError

import logging

logger = logging.getLogger(__name__)

class ErrorMiddleware(BaseMiddleware):
	async def __call__(self, handler, event, data):
		adminerror = data.get("adminerror", True)
		try:
			return await handler(event, data)

		except BotError as e:
			logger.warning(e.log(event))
			if adminerror:
				try:
					await event.answer(str(e))
				except TelegramBadRequest:
					pass

		except Exception:
			logger.exception("Unhandled exception")
			if adminerror:
				await event.answer("❌ Незарегистрированная ошибка")
