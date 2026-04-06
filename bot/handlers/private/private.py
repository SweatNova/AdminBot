from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter

router = Router()
router.message.filter(ChatTypeFilter(ChatType.PRIVATE))

@router.message(Command("start"))
async def start(message: Message):
	await message.reply("Привет!\n"
						"AdminBot это кастомный админ-бот который поможет тебе "
						"контролировать твою группу!\n\n" 
						"Добавь меня в группу чтобы увидеть функционал и сделай" 						" админом, в ЛС я даю только инструкцию\n\n"
						"Введите '/help' для получения инструкции")

@router.message(Command("help"))
async def help(message: Message):
	await message.reply("Привет!\n")		

@router.message()
async def all_another(message: Message):
	await message.reply("Неизвестная команда"
						", введите /help для получения инструкции")
