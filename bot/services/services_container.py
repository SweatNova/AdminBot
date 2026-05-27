from aiogram import Bot

from .services_list.admin_service import AdminService
from .services_list.bans_service import BansService
from .services_list.utils_service import UtilsService

from .services_list.core.members_service import MembersService
from .services_list.core.chats_settings_service import ChatsSettingsService
from .services_list.core.bot_chats_info_service import BotChatsInfoService
from .services_list.core.telegram_service import TelegramService

class ServicesContainer:
	def __init__(self, bot: Bot):
		self.members_service = MembersService()
		self.chats_settings_service = ChatsSettingsService()
		self.bot_chats_info_service = BotChatsInfoService()
		self.telegram_service = TelegramService(bot)

		self.admin_service = AdminService(
			self.members_service,
			self.chats_settings_service,
			self.telegram_service
		)
		self.bans_service = BansService(
			self.members_service,
			self.telegram_service
		)
		self.utils_service = UtilsService(
			self.members_service,
			self.telegram_service
		)
