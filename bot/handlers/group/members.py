from aiogram import Router
from aiogram.types import ChatMemberUpdated
from aiogram.enums import ChatType
from sqlalchemy import select

from bot.filters import ChatTypeFilter
from bot.utils import role_to_db
from bot.db.database import get_session
from bot.db.models import Member

from bot.utils import extract_admin_permissions, extract_user_permissions

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))

@router.chat_member()
async def chat_member_update(event: ChatMemberUpdated):
	chat_id = event.chat.id
	user = event.new_chat_member.user
	user_id = user.id
	username = user.username
	status = event.new_chat_member.status
	role = role_to_db(status)

	tg_member = None
	try:
		tg_member = await event.bot.get_chat_member(chat_id, user_id)
	except Exception:
		tg_member = None

	if tg_member and status in ("administrator", "creator"):
		admin_permissions = extract_admin_permissions(tg_member)
	else:
		admin_permissions = {}
	if tg_member and status not in ("left", "kicked"):
		user_permissions = extract_user_permissions(tg_member)
	else:
		user_permissions = {}

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
				role=role,
				admin_permissions=admin_permissions,
				user_permissions=user_permissions,
			)
			session.add(member)
		else:
			member.username = username
			member.role = role
			member.admin_permissions = admin_permissions
			member.user_permissions = user_permissions
