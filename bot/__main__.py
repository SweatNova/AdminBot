import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from bot.config_reader import get_config, BotConfig
from bot.handlers import get_routers
from bot.db import init_db

dp = Dispatcher()

async def main():
	bot_config = get_config(model=BotConfig, root_key="bot")
	bot = Bot(token=bot_config.token.get_secret_value())
	await init_db()
	for router in get_routers():
		dp.include_router(router)
	await dp.start_polling(
		bot,
		allowed_updates=["message", "chat_member", "my_chat_member"]
	)

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	asyncio.run(main())
