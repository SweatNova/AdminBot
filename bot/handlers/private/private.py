from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter

router = Router()
router.message.filter(ChatTypeFilter(ChatType.PRIVATE))

@router.message(Command("start"))
async def start(message: Message):
	await message.reply("Hello!\n"
						"AdminBot is a custom admin bot that helps you "
						"manage your group!\n\n"
						"Add me to your group to see the available features "
						"and grant me administrator rights. "
						"In private messages I only provide instructions.\n\n"
						"Enter '/help' to get the guide.")

@router.message(Command("help"))
async def help(message: Message):
	await message.reply("Hello!\n")

@router.message()
async def all_another(message: Message):
	await message.reply("Unknown command, "
						"enter /help to get the guide.")
