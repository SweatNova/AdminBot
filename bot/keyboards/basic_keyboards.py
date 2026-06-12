from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def all_help():
	builder = InlineKeyboardBuilder()
	buttons = [
		InlineKeyboardButton(text="Admin", callback_data="help_admin"),
		InlineKeyboardButton(text="AntiFlood", callback_data="help_antiflood"),
		InlineKeyboardButton(text="AntiRaid", callback_data="help_antiraid"),
		InlineKeyboardButton(text="Bans", callback_data="help_bans"),
		InlineKeyboardButton(text="Blocklist", callback_data="help_blocklist"),
		InlineKeyboardButton(text="Cleanup", callback_data="help_clean"),
		InlineKeyboardButton(text="Filters", callback_data="help_filters"),
		InlineKeyboardButton(text="Greetings",
							callback_data="help_greetings"),
		InlineKeyboardButton(text="Rules", callback_data="help_rules")
	]
	builder.row(*buttons[:3])
	builder.row(*buttons[3:6])
	builder.row(*buttons[6:9])
	return builder.as_markup()

def back_button(callback: str):
	builder = InlineKeyboardBuilder()
	builder.button(text="<-- Back", callback_data=callback + "_back")
	return builder.as_markup()
