import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from bot.config_reader import get_config, BotConfig

from bot.storages.postgre import init_db

from bot.services.services_container import ServicesContainer

from bot.handlers import get_routers

from bot.handlers.group.basic import set_commands

from bot.scheduler import Scheduler

dp = Dispatcher()

async def main():
	bot_config = get_config(model=BotConfig, root_key="bot")
	bot = Bot(token=bot_config.token.get_secret_value())
	await init_db()
	services_container = ServicesContainer(bot)
	dp["services"] = services_container
	for router in get_routers():
		dp.include_router(router)
	await set_commands(bot)
	scheduler = Scheduler(services_container)
	asyncio.create_task(scheduler.run())
	await dp.start_polling(bot)

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	asyncio.run(main())
