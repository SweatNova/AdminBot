from aiogram.types import Message, User
from aiogram import Bot
from bot.db.crud import get_member_by_username

async def is_admin(message: Message):
	member = await message.bot.get_chat_member(
		chat_id=message.chat.id,
		user_id=message.from_user.id
	)
	return member.status in ("administrator", "creator")

def status_to_db(status: str) -> str:
	mapping = {
		"creator": "creator",
        "administrator": "admin",
		"member": "user",
		"kicked": "kicked",
		"left": "left"
	}
	return mapping.get(status, "user")

def extract_admin_permissions(tg_member) -> dict:
	if tg_member.status == "creator":
		return {
			"all": True
		}
	return {
		"can_change_info": getattr(tg_member,
							"can_change_info", False),
		"can_delete_messages": getattr(tg_member,
							"can_delete_messages", False),
		"can_invite_users": getattr(tg_member,
							"can_invite_users", False),
		"can_restrict_members": getattr(tg_member,
							"can_restrict_members", False),
		"can_pin_messages": getattr(tg_member,
							"can_pin_messages", False),
		"can_promote_members": getattr(tg_member,
							"can_promote_members", False),
		"can_manage_video_chats": getattr(tg_member,
							"can_manage_video_chats", False),
		"can_manage_topics": getattr(tg_member,
							"can_manage_topics", False)
    }
def extract_user_permissions(tg_member) -> dict:
    return {
		"can_send_messages": getattr(tg_member,
							"can_send_messages", True),
		"can_send_media_messages": getattr(tg_member,
							"can_send_media_messages", True),
		"can_send_audios": getattr(tg_member,
							"can_send_audios", True),
		"can_send_voice_notes": getattr(tg_member,
							"can_send_voice_notes", True),
		"can_send_video_notes": getattr(tg_member,
							"can_send_video_notes", True),
		"can_send_polls": getattr(tg_member,
							"can_send_polls", True),
		"can_add_web_page_previews": getattr(tg_member,
							"can_add_web_page_previews", True),
		"can_invite_users": getattr(tg_member,
							"can_invite_users", True),
		"can_pin_messages": getattr(tg_member,
							"can_pin_messages", True),
		"can_change_info": getattr(tg_member,
							"can_change_info", True)
	}

async def get_username_or_id(session, chat_id: int, target: str):
    if target.startswith("@"):
        member = await get_member_by_username(
            session=session,
            chat_id=chat_id,
            username=target[1:]
        )
        if not member:
            raise ValueError("Пользователь не найден")
        return member.user_id, member.username
    elif target.isdigit():
        return int(target), None
    raise ValueError("Некорректный формат")
