from bot.storages.postgre.database import get_session
from bot.storages.postgre.crud_bot_chats_info import (
	get_bot_crud,
	get_bots_crud,
	create_bot_crud,
	delete_bot_crud,
)
from bot.storages.redis.cache import (
	get_cache,
	set_cache,
	delete_cache
)
from bot.storages.postgre.models import BotChatInfo

BOT_CHATS_INFO_TTL = 300

class BotChatsInfoService:
	@staticmethod
	def _key(chat_id: int) -> str:
		return f"bot:{chat_id}"
	@staticmethod
	def _bots_key() -> str:
		return f"bots:"
	@staticmethod
	def _serialize(bot: BotChatInfo) -> dict:
		return {
			"chat_id": bot.chat_id,
			"chat_type": bot.chat_type,
			"chat_username":bot.chat_username,
			"bot_role": bot.bot_role,
			"bot_user_permissions": bot.bot_user_permissions,
			"bot_admin_permissions": bot.bot_admin_permissions,
		}
	@staticmethod
	def _deserialize(data: dict) -> BotChatInfo:
		return BotChatInfo(**data)

	async def get_bot(self, chat_id: int) -> BotChatInfo:
		key = self._key(chat_id)
		cached = await get_cache(key)
		if cached:
			return self._deserialize(cached)

		async with get_session() as session:
			bot = await get_bot_crud(session, chat_id)
			if not bot:
				return None

		data = self._serialize(bot)
		await set_cache(key, BOT_CHATS_INFO_TTL, data)
		return bot

	async def get_bots(self) -> list[BotChatInfo]:
		key = self._bots_key()
		cached = await get_cache(key)
		if cached is not None:
			return [self._deserialize(b) for b in cached]

		async with get_session() as session:
			bots = await get_bots_crud(session)
	
		data = [self._serialize(b) for b in bots]
		await set_cache(key, BOT_CHATS_INFO_TTL, data)
		return bots

	async def upsert_bot(
		self, chat_id: int,
		chat_type: str,
		chat_username: str | None = None,
		bot_role: str | None = None,
		bot_user_permissions: dict | None = None,
		bot_admin_permissions: dict | None = None
	) -> BotChatInfo:
		async with get_session() as session:
			bot = await get_bot_crud(session, chat_id)
			if bot:
				bot.chat_type = chat_type
				bot.chat_username = chat_username
				bot.bot_role = bot_role
				bot.bot_user_permissions = bot_user_permissions
				bot.bot_admin_permissions = bot_admin_permissions
			else:
				bot = await create_bot_crud(session, chat_id,
											chat_type,
											chat_username,
											bot_role,
											bot_user_permissions,
											bot_admin_permissions)

		key = self._key(chat_id)
		data = self._serialize(bot)
		await set_cache(key, BOT_CHATS_INFO_TTL, data)
		await delete_cache(self._bots_key())
		return bot

	async def delete_bot(self, chat_id: int) -> None:
		async with get_session() as session:
			await delete_bot_crud(session, chat_id)

		key = self._key(chat_id)
		await delete_cache(key)
		await delete_cache(self._bots_key())
