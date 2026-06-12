from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter

from bot.keyboards.basic_keyboards import all_help, back_button

from aiogram.types import BotCommand

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Introduction message"),
        BotCommand(command="help", description="Help for all commands"),
		BotCommand(command="info", description="Bot information"),
		BotCommand(command="privacy", description="Coming soon"),

		BotCommand(command="promote", description="Promote to admin"),
        BotCommand(command="demote", description="Demote to user"),
        BotCommand(command="adminlist", description="Show admin list"),
        BotCommand(command="anonadmin", description="Toggle setting"),
        BotCommand(command="adminerror", description="Toggle setting"),

		BotCommand(command="kickme", description="Self kick"),
        BotCommand(command="ban", description="Ban"),
        BotCommand(command="dban", description="Ban and delete message"),
        BotCommand(command="sban", description="Silent ban"),
		BotCommand(command="unban", description="Unban"),
        BotCommand(command="mute", description="Mute"),
        BotCommand(command="dmute", description="Mute and delete message"),
        BotCommand(command="smute", description="Silent mute"),
        BotCommand(command="unmute", description="Unmute"),
        BotCommand(command="kick", description="Kick"),
        BotCommand(command="dkick", description="Kick and delete message"),
        BotCommand(command="skick", description="Silent kick"),
    ]
    await bot.set_my_commands(commands)

@router.message(Command("start"))
async def start(message: Message):
	await message.answer(
		"Hello, I'm AdminBot, a group administration bot!\n\n"
		"Use /help to get information about all commands or "
		"/info to learn more about the bot.\n"
		"Also use /privacy to view our privacy policy."
	)

@router.message(Command("help"))
async def help(message: Message):
	await message.answer(
		"----- Help ----- \n\n"
		"This command displays the full list of available commands "
		"grouped by category.\n\n"
		"Tip: you can view all commands by typing / !",
		reply_markup=all_help()
	)

@router.callback_query(F.data.startswith("help_"))
async def help_callback(callback: CallbackQuery):
	if callback.data == "help_admin":
		await callback.message.edit_text(
			"---- Admin ---- \n\n"
			"Here you can find all commands related to administrator "
			"management and permissions.\n\n"
			"Commands:\n"
			"-/promote <reply/username>:\n"
			"Promote a user to administrator.\n"
			"-/demote <reply/username>:\n"
			"Demote an administrator to a regular member.\n"
			"-/adminlist:\n"
			"Show the list of administrators.\n"
			"-/anonadmin <on/off>:\n"
			"Handle anonymous administrators with full permissions, "
			"disabled by default and not recommended to change.\n"
			"-/adminerror <on/off>:\n"
			"Enable or disable error messages when regular users "
			"attempt to use admin commands. Enabled by default.",
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
			"Here you can find commands for user management, "
			"moderation, and permissions.\n\n"
			"Note: arguments enclosed in {} are optional.\n\n"
			"Commands:\n"
			"-/kickme:\n"
			"A user can remove themselves from the chat.\n"
			"-/ban <reply/username> {time}:\n"
			"Ban a user.\n"
			"-/dban <reply/username> {time}:\n"
			"Ban a user and delete their message.\n"
			"-/sban <reply/username> {time}:\n"
			"Silent ban with deletion of the bot message.\n"
			"-/unban <reply/username>:\n"
			"Unban a user.\n"
			"-/mute <reply/username> {time}:\n"
			"Restrict a user from sending messages.\n"
			"-/dmute <reply/username> {time}:\n"
			"Restrict a user and delete their message.\n"
			"-/smute <reply/username> {time}:\n"
			"Silent restriction with deletion of the bot message.\n"
			"-/unmute <reply/username>:\n"
			"Remove restrictions from a user.\n"
			"-/kick <reply/username>:\n"
			"Remove a user from the chat.\n"
			"-/dkick <reply/username>:\n"
			"Remove a user and delete their message.\n"
			"-/skick <reply/username>:\n"
			"Silent removal with deletion of the bot message.\n",
			reply_markup=back_button("help")
		)
	if callback.data == "help_back":
		await callback.message.edit_text(
			"----- Help -----\n\n"
			"This command displays the full list of available commands "
			"grouped by category.\n\n"
			"Tip: you can view all commands by typing / !",
			reply_markup=all_help()
		)

@router.message(Command("info"))
async def info(message: Message):
	await message.answer(
		"🤖 <b>AdminBot</b>\n\n"
		"📌 <b>Description:</b>\n"
		"Bot for group administration and management.\n\n"
		"👤 <b>Author:</b>\n"
		"@F3m_b0y\n\n"
		"📦 <b>Version:</b>\n"
		"0.5.2\n\n"
		"⚖️ <b>License:</b>\n"
		"MIT",
		parse_mode="HTML"
	)
