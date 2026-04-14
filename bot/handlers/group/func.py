from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramBadRequest

from bot.filters import ChatTypeFilter
from bot.db.database import get_session
from bot.db.crud import upsert_member, get_member_by_username
from bot.utils import is_admin, extract_admin_permissions

RIGHTS_ADMIN = {
	"can_change_info": True,
	"can_delete_messages": True,
	"can_invite_users": True,
	"can_restrict_members": True,
	"can_pin_messages": True,
	"can_promote_members": False,
}
RIGHTS_MEMBER = {
	"can_change_info": False,
	"can_delete_messages": False,
	"can_invite_users": False,
	"can_restrict_members": False,
	"can_pin_messages": False,
	"can_promote_members": False,
}

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))

async def change_role(bot: Bot, session, chat_id: int,
						 target: str, command: str):
	user_id = None
	username = None
	if target.startswith("@"):
		member = await get_member_by_username(
			session=session,
			chat_id=chat_id,
			username=target[1:]
		)
		if not member:
			return f"❌ Пользователь {target} не найден"
		user_id = member.user_id
		username = member.username
	elif target.isdigit():
		user_id = int(target)
	else:
		return "❌ Некорректный формат"
	try:
		tg_member = await bot.get_chat_member(chat_id, user_id)
		if tg_member.user.is_bot:
			return "❌ Нельзя менять права у ботов"
		rights = RIGHTS_ADMIN if command == "/promote" else RIGHTS_MEMBER
		role = "administrator" if command == "/promote" else "member"
		action = "повышен" if command == "/promote" else "понижен"

		await bot.promote_chat_member(
			chat_id=chat_id, 
			user_id=user_id, 
			**rights
		)
		await upsert_member(
			session=session,
			chat_id=chat_id,
			user_id=user_id,
			username=username,
			role=role,
			user_permissions={},
			admin_permissions=extract_admin_permissions(tg_member) 
				if role == "administrator"
				else {}
		)
		return f"✅ Пользователь {action} до {role}"
	except TelegramBadRequest as e:
		return f"❌ Ошибка telegram: {e}"

@router.message(F.text.startswith(("/promote", "/demote")))
async def promote_user(message: Message, bot: Bot):
	args = message.text.split(maxsplit=1)
	if len(args) < 2:
		return await message.reply("Введите айди или юзернейм")
	if not await is_admin(message):
		return await message.answer("❌ Недостаточно прав")
	async with get_session() as session:
		result = await change_role(
			bot=bot,
			session=session,
			chat_id=message.chat.id,
			target=args[1],
			command=args[0]
		)
	await message.reply(result)
