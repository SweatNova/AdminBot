from __future__ import annotations

from aiogram.types import Message, ChatPermissions
from aiogram.exceptions import TelegramBadRequest

from datetime import datetime

class BansService:
	def __init__(
		self,
		members_service: MembersService,
		telegram_service: TelegramService
	):
		self.members_service = members_service
		self.telegram_service = telegram_service

	async def ban(self, chat_id: int, user_id: int, username: str,
				  message: Message,
				  delete: bool = False, secret: bool = False,
				  until_date: datetime | None = None) -> str:
		try:
			if await self.telegram_service.is_admin(chat_id, user_id):
				return "❌ Нельзя банить админов"

			if delete:
				if not message.reply_to_message:
					return "❌ Команда требует реплая на сообщение"
				await self.telegram_service.delete_message(
					chat_id,
					message.reply_to_message.message_id
				)

			await self.telegram_service.ban_chat_member(
				chat_id,
				user_id,
				until_date
			)

			if secret:
				await self.telegram_service.delete_message(
					chat_id,
					message.message_id
				)

			user = message.from_user
			await self.members_service.update_punishments(
				chat_id,
				user_id,
				"banned",
				f"@{user.username}" if user.username else user.full_name,
				datetime.utcnow(),
				until_date
			)
			return f"✅ Пользователь {username} забанен"

		except TelegramBadRequest as e:
			return f"❌ Telegram ошибка: {e}"

	async def unban(self, chat_id: int, user_id: int, username: str) -> str:
		try:
			member = await self.telegram_service.get_chat_member(
				chat_id,
				user_id
			)
			if member.status != "kicked":
				return "❌ Нельзя анбанить незабанненных юзеров"

			await self.telegram_service.unban_chat_member(chat_id, user_id)
			await self.members_service.update_punishments(
				chat_id,
				user_id,
				None,
				None,
				None,
				None
			)
			return f"✅ Пользователь {username} разбанен"

		except TelegramBadRequest as e:
			return f"❌ Telegram ошибка: {e}"

	async def mute(self, chat_id: int, user_id: int, username: str,
				   message: Message,
				   delete: bool = False, secret: bool = False,
				   until_date: datetime | None = None) -> str:
		try:
			if await self.telegram_service.is_admin(chat_id, user_id):
				return "❌ Нельзя мутить админов"

			if delete:
				if not message.reply_to_message:
					return "❌ Команда требует реплая на сообщение"
				await self.telegram_service.delete_message(
					chat_id,
					message.reply_to_message.message_id
				)

			await self.telegram_service.restrict_chat_member(
				chat_id=chat_id,
				user_id=user_id,
				permissions=ChatPermissions(
					can_send_messages=False,
					can_send_polls=False,
					can_change_info=False,
					can_send_audios=False,
					can_send_photos=False,
					can_send_videos=False,
					can_invite_users=False,
					can_pin_messages=False,
					can_manage_topics=False,
					can_send_documents=False,
					can_send_video_notes=False,
					can_send_voice_notes=False,
					can_send_other_messages=False,
					can_add_web_page_previews=False
				),
				until_date=until_date
			)

			if secret:
				await self.telegram_service.delete_message(
					chat_id,
					message.message_id
				)

			user = message.from_user
			await self.members_service.update_punishments(
				chat_id,
				user_id,
				"muted",
				f"@{user.username}" if user.username else user.full_name,
				datetime.utcnow(),
				until_date
			)
			return f"✅ Пользователь {username} замучен"

		except TelegramBadRequest as e:
			return f"❌ Telegram ошибка: {e}"

	async def unmute(self, chat_id: int, user_id: int, username: str) -> str:
		try:
			if await self.telegram_service.is_admin(chat_id, user_id):
				return "❌ Нельзя анмутить админов"

			await self.telegram_service.restrict_chat_member(
				chat_id=chat_id,
				user_id=user_id,
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
			await self.members_service.update_punishments(
				chat_id,
				user_id,
				None,
				None,
				None,
				None
			)		
			return f"✅ Пользователь {username} размучен"

		except TelegramBadRequest as e:
			return f"❌ Telegram ошибка: {e}"
		message

	async def kick(self, chat_id: int, user_id: int, username: str,
				   message: Message,
				   delete: bool = False, secret: bool = False) -> str:
		try:
			if await self.telegram_service.is_admin(chat_id, user_id):
				return "❌ Нельзя кикать админов"

			if delete:
				if not message.reply_to_message:
					return "❌ Команда требует реплая на сообщение"			
				await self.telegram_service.delete_message(
					chat_id,
					message.reply_to_message.message_id
				)

			await self.telegram_service.ban_chat_member(chat_id, user_id)
			await self.telegram_service.unban_chat_member(chat_id, user_id)

			if secret:
				await self.telegram_service.delete_message(
					chat_id,
					message.message.id
				)
			return f"✅ Пользователь {username} кикнут"

		except TelegramBadRequest as e:
			return f"❌ Telegram ошибка: {e}"

	async def kickme(self, chat_id, user_id, username) -> str:
		try:
			if await self.telegram_service.is_admin(chat_id, user_id):
				return "❌ Вы админ! лишите себя прав для выполнения команды"

			await self.telegram_service.ban_chat_member(chat_id, user_id)
			await self.telegram_service.unban_chat_member(chat_id, user_id)
			return f"✅ Пользователь {username} вышел из чата"

		except TelegramBadRequest as e:
			return f"❌ Telegram ошибка: {e}"
