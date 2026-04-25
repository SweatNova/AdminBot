from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.enums import ChatType
from bot.filters import ChatTypeFilter
from aiogram.exceptions import TelegramBadRequest

from bot.db.database import get_session
from bot.db.crud import upsert_member
from bot.db.crud_settings import upsert_settings, get_settings
from bot.utils import (
	extract_admin_permissions,
	get_username_or_id,
	chat_settings_switch,
)
from bot.middleware import AdminMiddleware

router = Router()
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
router.message.middleware(AdminMiddleware())

async def change_role(bot: Bot, session, chat_id: int,
					  command: str, target: str):
	RIGHTS_ADMIN = {
		"can_change_info": True,
		"can_delete_messages": True,
		"can_invite_users": True,
		"can_restrict_members": True,
		"can_pin_messages": True,
		"can_promote_members": False
	}
	RIGHTS_MEMBER = {
		"can_change_info": False,
		"can_delete_messages": False,
		"can_invite_users": False,
		"can_restrict_members": False,
		"can_pin_messages": False,
		"can_promote_members": False
	}

	user_id, username = await get_username_or_id(session, chat_id, target)

	target_member = await bot.get_chat_member(chat_id, user_id)
	if target_member.user.is_bot:
		return "❌ Нельзя менять права у ботов"

	rights = RIGHTS_ADMIN if command == "/promote" else RIGHTS_MEMBER
	role = "admin" if command == "/promote" else "user"
	action = "повышен" if command == "/promote" else "понижен"

	try:
		await bot.promote_chat_member(
			chat_id=chat_id,
			user_id=user_id,
			**rights
		),
		await upsert_member(
			session=session,
			chat_id=chat_id,
			user_id=user_id,
			username=username,
			role=role,
			user_permissions={},
			admin_permissions=extract_admin_permissions(target_member)
			if role == "admin" else {}
		)
		return f"✅ Пользователь {action} до {role}"
	except TelegramBadRequest as e:
		return f"❌ Ошибка telegram: {e}"

@router.message(F.text.startswith(("/promote", "/demote")))
async def promote_demote_user(message: Message, bot: Bot):
	args = message.text.split(maxsplit=1)
	if len(args) != 2:
		return await message.reply("Введите айди или юзернейм")

	async with get_session() as session:
		result = await change_role(
			bot=bot,
			session=session,
			chat_id=message.chat.id,
			command=args[0],
			target=args[1]
		)
	await message.reply(result)

@router.message(F.text == "/adminlist", flags={"skip_admin": True})
async def admin_list(message: Message, bot: Bot):
	admins = await bot.get_chat_administrators(message.chat.id)
	text = "\n".join(
		f"{a.status} | {a.user.id} | @{a.user.username or 'no_username'}"
		for a in admins
	)
	await message.reply("✅ Вот весь список админов чата: \n" + text)

@router.message(F.text.startswith("/anonadmin"))
async def anon_admin(message: Message, bot: Bot):
	await chat_settings_switch(message, bot, "admin")
@router.message(F.text.startswith("/adminerror"))
async def admin_error(message: Message, bot: Bot):
	await chat_settings_switch(message, bot, "admin")
