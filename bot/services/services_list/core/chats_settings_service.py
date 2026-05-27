from bot.storages.postgre.database import get_session
from bot.storages.postgre.crud_chats_settings import (
	get_settings_crud,
	get_all_settings_crud,
	create_settings_crud,
	delete_settings_crud,
)
from bot.storages.redis.cache import (
	get_cache,
	set_cache,
	delete_cache
)
from bot.storages.postgre.models import ChatSettings

CHATS_SETTINGS_TTL = 300

class ChatsSettingsService:
	@staticmethod
	def _key(chat_id: int) -> str:
		return f"settings:{chat_id}"
	@staticmethod
	def _all_settings_key() -> str:
		return f"all_settings:"
	@staticmethod
	def _serialize(settings: ChatSettings) -> dict:
		return {
			"chat_id": settings.chat_id,
			"admin": settings.admin
		}
	@staticmethod
	def _deserialize(data: dict) -> ChatSettings:
		return ChatSettings(**data)

	async def get_settings(self, chat_id: int) -> ChatSettings:
		key = self._key(chat_id)
		cached = await get_cache(key)
		if cached:
			return self._deserialize(cached)

		async with get_session() as session:
			settings = await get_settings_crud(session, chat_id)
			if not settings:
				return None

		data = self._serialize(settings)
		await set_cache(key, CHATS_SETTINGS_TTL, data)
		return settings

	async def get_all_settings(self) -> list[ChatSettings]:
		key = self._all_settings_key()
		cached = await get_cache(key)
		if cached is not None:
			return [self._deserialize(s) for s in cached]

		async with get_session() as session:
			all_settings = await get_all_settings_crud(session)
	
		data = [self._serialize(s) for s in all_settings]
		await set_cache(key, CHATS_SETTINGS_TTL, data)
		return all_settings

	async def upsert_settings(
		self,
		chat_id: int,
		admin: dict | None = None
	) -> ChatSettings:
		async with get_session() as session:
			settings = await get_settings_crud(session, chat_id)

			if settings:
				if admin is not None:
					settings.admin.update(admin)
			else:
				settings = await create_settings_crud(
					session,
					chat_id,
					admin
				)

		key = self._key(chat_id)
		data = self._serialize(settings)
		await set_cache(key, CHATS_SETTINGS_TTL, data)
		await delete_cache(self._all_settings_key())
		return settings

	async def delete_settings(self, chat_id: int) -> None:
		async with get_session() as session:
			await delete_settings_crud(session, chat_id)

		key = self._key(chat_id)
		await delete_cache(key)
		await delete_cache(self._all_settings_key())

	async def chat_settings_switch(self, chat_id: int, args: list,
								   settings_dict_name: str) -> str:
		if len(args) != 2:
			return "❌ Выберите режим on/off"
		if not args[1] in ["on", "off"]:
			return "❌ Неизвестный режим"

		async with get_session() as session:
			chat_settings = await get_settings_crud(session, chat_id)
			value = getattr(chat_settings, settings_dict_name, None)
			settings_dict = dict(value)
			setting = args[0][1:]
			if args[1] == "on":
				settings_dict[setting] = True
				text = "включенна"
			else:
				settings_dict[setting] = False
				text = "выключенна"
		await self.upsert_settings(chat_id, settings_dict)
		return f"✅ Настройка {args[0]} теперь {text}"
