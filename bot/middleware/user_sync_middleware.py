from aiogram import BaseMiddleware

from bot.services.services_container import ServicesContainer

class UserSyncMiddleware(BaseMiddleware):
	async def __call__(self, handler, event, data):
		message = event.message
		if message is None:
			return await handler(event, data)

		services: ServicesContainer = data["services"]

		chat_id = message.chat.id
		user_id = message.from_user.id
		username = message.from_user.username

		member = await services.members_service.get_member(chat_id, user_id)
		if member is None:
			tg_member = await services.telegram_service.get_chat_member(
				chat_id,
				user_id
			)
			role = services.telegram_service.status_to_role_db(tg_member.status)
			user_permissions = (
				services.telegram_service.extract_user_permissions(tg_member)
			)
			admin_permissions = (
				services.telegram_service.extract_admin_permissions(tg_member)
			)
			await services.members_service.upsert_member(
				chat_id,
				user_id,
				username,
				role,
				user_permissions,
				admin_permissions	
			)
		return await handler(event, data)

