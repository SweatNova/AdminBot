from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter

from bot.db import get_session
from bot.db.crud_settings import upsert_settings, get_settings

from bot.keyboards.basic_keyboards import all_help, back_button

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))

@router.message(Command("start"))
async def start(message: Message):
	await message.answer(
		"Привет, я бот-администратор AdminBot!\n\n"
		"Введите команду /help для получения информации о всех" 						" командах или /info для получения информации о боте"
		"\n\nТакже введите /privacy для получения информации о" 						" нашей политике конфиденциальности"
	)

@router.message(Command("help"))
async def help(message: Message):
	await message.answer(
		"----- Help -----\n\nДанная команда "
		"показывает весь список доступных команд "
		"по категориям\n\nПодсказка: все команды "
		"вы можете увидеть набрав '/'!", 
		reply_markup=all_help()
	)

@router.callback_query(F.data.startswith("help_"))
async def help_callback(callback: CallbackQuery):
	if callback.data == "help_admin":
		await callback.message.edit_text(
			"---- Admin ---- \n\nЗдесь собраны всех команды по управлению "
			"администраторскими полномочиями и правами \n\n"
			"Команды: \n-/promote <reply/username>: \nПовысить пользователя " 
			"до администратора. \n-/demote <reply/username>:\nПонизить "
			"администратора до участника. \n-/adminlist: Показать список "
			"админов.\n"
			"-/anonadmin <on/off>: \nОбрабатывать анонимных админов с полными "				"правами, по умолчанию включено, не рекомендуется менять.\n"
			"-/adminerror <on/off>: \nОтправлять или нет ошибки при вызове "
			"админ команд обычными юзерами. по умолчанию включено.",
			reply_markup=back_button("help")
		)
	if callback.data == "help_antiflood":
		pass
	if callback.data == "help_back":
		await callback.message.edit_text(
			"----- Help -----\n\nДанная команда "
			"показывает весь список доступных команд "
			"по категориям\n\nПодсказка: все команды "
			"вы можете увидеть набрав '/'!",
			reply_markup=all_help()
		)

@router.message(Command("info"))
async def info(message: Message):
    await message.answer(
        "ℹ️ Информация о боте\n\n"
        "Автор: @F3m_b0y\n"
        "Лицензия: MIT\n"
        "Описание: Этот бот помогает администрировать вашу группу.\n"
        "Версия: 0.4.1"
	)

