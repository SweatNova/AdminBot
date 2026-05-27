import asyncio
from datetime import datetime

from bot.storages.postgre.database import get_session
from bot.storages.postgre.crud_members import get_punishments_crud
from aiogram.types import ChatPermissions

from bot.services.services_container import ServicesContainer

class Scheduler:
	def __init__(self, services: ServicesContainer):
		self.services = services

	async def run(self):
		while True:
			members_service = self.services.members_service
			telegram_service = self.services.telegram_service
			async with get_session() as session:
				users = await get_punishments_crud(session, datetime.utcnow())
			for user in users:
				try:
					if user.restricted_status == "banned":
						await telegram_service.unban_chat_member(
							user.chat_id,
							user.user_id
						)
					elif user.restricted_status == "muted":
						await telegram_service.restrict_chat_member(
							chat_id=user.chat_id,
							user_id=user.user_id,
							permissions=ChatPermissions(
								can_send_messages=True,
								can_send_polls=True,
								can_change_info=False,
								can_send_audios=True,
								can_send_photos=True,
								can_send_videos=True,
								can_invite_users=True,
								can_pin_messages=False,
								can_manage_topics=False,
								can_send_documents=True,
								can_send_video_notes=True,
								can_send_voice_notes=True,
								can_send_other_messages=True,
								can_add_web_page_previews=True,
							)
						)

					await members_service.update_punishments(
						user.chat_id,
						user.user_id,
						None,
						None,
						None,
						None
					)
				except Exception as e:
					print(f"Scheduler error {user.chat_id}:{user.user_id}: {e}")
			await asyncio.sleep(30)
