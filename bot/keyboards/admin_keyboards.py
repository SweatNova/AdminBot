from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Помощь", callback_data="help")],
        [InlineKeyboardButton(text="Информация", callback_data="info")],
        [InlineKeyboardButton(text="Настройки", callback_data="settings")]
    ])
    return kb
def all_help():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Админ", callback_data="help_admin")],
        [InlineKeyboardButton(text="АнтиФлуд", callback_data="help_antiflood")],
        [InlineKeyboardButton(text="АнтиРейд", callback_data="help_antiraid")],
		[InlineKeyboardButton(text="Баны", callback_data="help_bans")],
		[InlineKeyboardButton(text="Блоклист", callback_data="help_blocklist")],
		[InlineKeyboardButton(text="Очистка", callback_data="help_clean")],
		[InlineKeyboardButton(text="Фильтры", callback_data="help_filters")],
		[InlineKeyboardButton(text="Привет!", callback_data="help_greetings")]
    ])
    return kb
