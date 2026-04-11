from aiogram.types import Message, User
from aiogram import Bot

async def is_admin(message: Message):
    member = await message.bot.get_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id
    )    
    return member.status in ("administrator", "creator")

def role_to_db(status: str) -> str:
    if status == "administrator":
        return "admin"
    elif status == "member":
        return "user"
    elif status == "left":
        return "left"
    elif status == "kicked":
        return "kicked"
    elif status == "banned":
        return "kicked"
    else:
        return "user"
