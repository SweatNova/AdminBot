from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def all_help():
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="Админ", callback_data="help_admin"),
        InlineKeyboardButton(text="АнтиФлуд", callback_data="help_antiflood"),
        InlineKeyboardButton(text="АнтиРейд", callback_data="help_antiraid"),
        InlineKeyboardButton(text="Баны", callback_data="help_bans"),
        InlineKeyboardButton(text="Блоклист", callback_data="help_blocklist"),
        InlineKeyboardButton(text="Очистка", callback_data="help_clean"),
        InlineKeyboardButton(text="Фильтры", callback_data="help_filters"),
        InlineKeyboardButton(text="Приветствия",
							 callback_data="help_greetings"),
        InlineKeyboardButton(text="Правила", callback_data="help_rules")
    ]
    builder.row(*buttons[:3])
    builder.row(*buttons[3:6])
    builder.row(*buttons[6:9])
    return builder.as_markup()

def back_button(callback: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="<-- Вернутся", callback_data=callback + "_back")
    return builder.as_markup()
