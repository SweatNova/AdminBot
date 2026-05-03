from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter

from bot.db import get_session
from bot.db.crud_settings import upsert_settings, get_settings

from bot.keyboards.basic_keyboards import all_help, back_button

from aiogram.types import BotCommand

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Ознакомительное сообщения"),
        BotCommand(command="help", description="Справка по всем командам"),
		BotCommand(command="info", description="Информация о боте"),
		BotCommand(command="privacy", description="Coming soon"),

		BotCommand(command="promote", description="Повысить до админа"),
        BotCommand(command="demote", description="Понизить до юзера"),
        BotCommand(command="adminlist", description="Вывод списка админов"),
        BotCommand(command="anonadmin", description="Переключить настройку"),
        BotCommand(command="adminerror", description="Переключить настройку"),

		BotCommand(command="kickme", description="Самокик"),
        BotCommand(command="ban", description="Бан"),
        BotCommand(command="dban", description="Бан с удалением сообщения"),
        BotCommand(command="sban", description="Скрытый бан"),
		BotCommand(command="unban", description="Разбан"),
        BotCommand(command="mute", description="Мут"),
        BotCommand(command="dmute", description="Мут с удалением сообщения"),
        BotCommand(command="smute", description="Скрытый мут"),
        BotCommand(command="unmute", description="Размут"),
        BotCommand(command="kick", description="Кик"),
        BotCommand(command="dkick", description="Кик с удалением сообщения"),
        BotCommand(command="skick", description="Скрытый кик"),
    ]
    await bot.set_my_commands(commands)

@router.message(Command("start"))
async def start(message: Message):
	await message.answer(
		"Привет, я бот-администратор AdminBot!\n\n"
		"Введите команду /help для получения информации о всех командах или "
		"/info для получения информации о боте \n"
		"Также введите /privacy для получения информации о нашей политике"
		"конфиденциальности"
	)

@router.message(Command("help"))
async def help(message: Message):
	await message.answer(
		"----- Help ----- \n\n"
		"Данная команда показывает весь список доступных команд по "
		"категориям \n\n"
		"Подсказка: все команды вы можете увидеть набрав / !", 
		reply_markup=all_help()
	)

@router.callback_query(F.data.startswith("help_"))
async def help_callback(callback: CallbackQuery):
	if callback.data == "help_admin":
		await callback.message.edit_text(
			"---- Admin ---- \n\n"
			"Здесь собраны всех команды по управлению администраторскими"
			"полномочиями и правами \n\n"
			"Команды: \n"
			"-/promote <reply/username>: \n"
			"Повысить пользователя до администратора. \n"
			"-/demote <reply/username>: \n"
			"Понизить администратора до участника. \n"
			"-/adminlist: \n"
			"Показать список админов. \n"
			"-/anonadmin <on/off>: \n"
			"Обрабатывать анонимных админов с полными правами," 
			"по умолчанию выключено, не рекомендуется менять. \n"
			"-/adminerror <on/off>: \n"
			"Отправлять или нет ошибки при вызове админ команд обычными юзерами, 			по умолчанию включено.",
			reply_markup=back_button("help")
		)
	if callback.data == "help_antiflood":
		pass
	if callback.data == "help_antiraid":
		pass
	if callback.data == "help_approval":
		pass
	if callback.data == "help_bans":
		await callback.message.edit_text(
			"---- Bans ---- \n\n"
			"Здесь собраны команды для управления пользователями, "
			"модерацией и правами. \n\n"
			"Примечание: аргументы в фигурных скобках {} "
			"не являются обязательными \n\n"
			"Команды: \n"
			"-/kickme: \n"
			"Пользователь может сам себя исключить из чата. \n"
			"-/ban <reply/username> {time}: \n"
			"Заблокировать пользователя. \n"
			"-/dban <reply/username> {time}: \n"
			"Заблокировать пользователя и удалить его сообщение. \n"
			"-/sban <reply/username> {time}: \n"
			"Скрытая блокировка пользователя с удалением сообщения бота \n"
			"-/unban <reply/username>: \n"
			"Разблокировать пользователя. \n"
			"-/mute <reply/username> {time}: \n"
			"Ограничить отправку сообщений пользователю. \n"
			"-/dmute <reply/username> {time}: \n"
			"Ограничить пользователя с удалением его сообщения. \n"
			"-/smute <reply/username> {time}: \n"
			"Скрытое ограничение пользователя с удалением сообщения бота \n"
			"-/unmute <reply/username>: \n"
			"Снять ограничения с пользователя. \n"
			"-/kick <reply/username>: \n"
			"Исключить пользователя из чата. \n"
			"-/dkick <reply/username>: \n"
			"Исключить пользователя с удалением сообщения. \n"
			"-/skick <reply/username>: \n"
			"Скрытое исключение пользователя с удалением сообщения бота\n",
			reply_markup=back_button("help")
		)
	if callback.data == "help_back":
		await callback.message.edit_text(
			"----- Help -----\n\n"
			"Данная команда показывает весь список доступных команд "
			"по категориям \n\n"
			"Подсказка: все команды вы можете увидеть набрав / !",
			reply_markup=all_help()
		)

@router.message(Command("info"))
async def info(message: Message):
    await message.answer(
        "ℹ️ Информация о боте\n\n"
        "Автор: @F3m_b0y\n"
        "Лицензия: MIT\n"
        "Описание: Этот бот помогает администрировать вашу группу.\n"
        "Версия: 0.4.8"
	)

