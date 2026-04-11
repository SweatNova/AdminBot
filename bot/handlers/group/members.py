from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.enums import ChatType

from aiogram.types import ChatMemberUpdated
from sqlalchemy import select

from bot.filters import ChatTypeFilter
from bot.utils import role_to_db

from bot.db.database import get_session
from bot.db.models import Member

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))

@router.chat_member()
async def chat_member_update(event: ChatMemberUpdated):
    chat_id = event.chat.id
    user_id = event.new_chat_member.user.id
    username = event.new_chat_member.user.username
    role = role_to_db(event.new_chat_member.status)

    async with get_session() as session:
        result = await session.execute(
            select(Member).where(
                Member.chat_id == chat_id,
                Member.user_id == user_id
            )
        )
        member = result.scalar_one_or_none()
        if member is None:
            member = Member(
                chat_id=chat_id,
                user_id=user_id,
                username=username,
                role=role
            )
            session.add(member)
        else:
            member.username = username
            member.role = role

