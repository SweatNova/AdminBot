from aiogram import BaseMiddleware

import time

class ResponseTimeMiddleware(BaseMiddleware):
	async def __call__(self, handler, event, data):
		data["request_start"] = time.perf_counter()
		return await handler(event, data)
