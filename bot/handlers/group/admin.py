from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter
from aiogram.types import ChatMemberAdministrator, ChatMemberOwner

from ...keyboards.admin_keyboards import start_menu, all_help

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))

#сначала идут вспомогательные функции - затем хендлеры на сообщения/команды
#после - хендлеры на колбеки 

async def bot_has_permission(bot, chat_id, permission: str) -> bool:
    member = await bot.get_chat_member(chat_id, bot.id)

    if isinstance(member, (ChatMemberAdministrator, ChatMemberOwner)):
        return getattr(member, permission, True)
    else:
        return False

@router.message(Command("start"))
async def start(message: Message):
	await message.answer("Привет, я бот-администратор твоей группы "
						 "AdminBot!\n\n"
						 "Выберите действие ниже", reply_markup=start_menu())

@router.message(Command("ban"))

@router.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
	await callback.message.edit_text("----- Help -----\n\nДанная команда "
									 "показывает весь список доступных команд "
									 "по категориям\n\nПодсказка: все команды "
									 "вы можете увидеть набрав '/'!", 
									 reply_markup=all_help())
