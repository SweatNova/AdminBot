from bot.storages.postgre.database import get_session
from bot.storages.postgre.crud_members import (
	get_member_crud,
	get_member_by_username_crud,
	get_members_crud,
	create_member_crud,
	delete_member_crud,
	get_punishments_crud
)
from bot.storages.redis.cache import (
	get_cache,
	set_cache,
	delete_cache
)
from bot.storages.postgre.models import Member

MEMBERS_TTL = 60

class MembersService:
	@staticmethod
	def _key(chat_id: int, user_id: int) -> str:
		return f"member:{chat_id}:{user_id}"
	@staticmethod
	def _username_key(chat_id: int, username: str) -> str:
		return f"member:{chat_id}:{username}"
	@staticmethod
	def _members_key(chat_id: int) -> str:
		return f"members:{chat_id}"
	@staticmethod
	def _serialize(member: Member) -> dict:
		return {
			"chat_id": member.chat_id,
			"user_id": member.user_id,
			"username": member.username,
			"role": member.role,
			"user_permissions": member.user_permissions,
			"admin_permissions": member.admin_permissions,
			"restricted_status": member.restricted_status,
			"admin_who_restricted": member.admin_who_restricted,
			"start_time": member.start_time,
			"end_time": member.end_time
		}
	@staticmethod
	def _deserialize(data: dict) -> Member:
		return Member(**data)

	async def get_member(self, chat_id: int, user_id: int) -> Member | None:
		key = self._key(chat_id, user_id)
		cached = await get_cache(key)
		if cached:
			return self._deserialize(cached)

		async with get_session() as session:
			member = await get_member_crud(session, chat_id, user_id)
			if not member:
				return None

		data = self._serialize(member)
		await set_cache(key, MEMBERS_TTL, data)
		return member

	async def get_member_by_username(
		self,
		chat_id: int,
		username: str
	) -> Member | None:
		key = self._username_key(chat_id, username)
		cached = await get_cache(key)
		if cached:
			return self._deserialize(cached)

		async with get_session() as session:
			member = await get_member_by_username_crud(
				session,
				chat_id,
				username
			)
			if not member:
				return None

		data = self._serialize(member)
		await set_cache(key, MEMBERS_TTL, data)
		return member

	async def get_members(self, chat_id: int) -> list[Member]:
		key = self._members_key(chat_id)
		cached = await get_cache(key)
		if cached:
			return [self._deserialize(m) for m in cached]

		async with get_session() as session:
			members = await get_members_crud(session, chat_id)
	
		data = [self._serialize(m) for m in members]
		await set_cache(key, MEMBERS_TTL, data)
		return members

	async def upsert_member(
		self,
		chat_id: int,
		user_id: int,
		username: str | None = None,
		role: str | None = None,
		user_permissions: dict | None = None,
		admin_permissions: dict | None = None
	) -> Member | None:
		async with get_session() as session:
			member = await get_member_crud(session, chat_id, user_id)
			if member:
				member.username = username
				member.role = role
				member.user_permissions = user_permissions
				member.admin_permissions = admin_permissions
			else:
				member = await create_member_crud(
					session,
					chat_id,
					user_id,
					username,
					role,
					user_permissions,
					admin_permissions,
					None,
					None,
					None,
					None
				)

		key = self._key(chat_id, user_id)
		data = self._serialize(member)
		await set_cache(key, MEMBERS_TTL, data)
		await delete_cache(self._members_key(chat_id))
		return member

	async def delete_member(self, chat_id: int, user_id: int) -> None:
		async with get_session() as session:
			await delete_member_crud(session, chat_id, user_id)

		key = self._key(chat_id, user_id)
		await delete_cache(key)
		await delete_cache(self._members_key(chat_id))
	
	async def update_punishments(
		self,
		chat_id: int,
		user_id: int,
		restricted_status: str | None = None,
		admin_who_restricted: str | None = None,
		start_time=None,
		end_time=None
	) -> Member:
		async with get_session() as session:
			member = await get_member_crud(session, chat_id, user_id)
			member.restricted_status = restricted_status
			member.admin_who_restricted = admin_who_restricted
			member.start_time = start_time
			member.end_time = end_time

		key = self._key(chat_id, user_id)
		data = self._serialize(member)
		await set_cache(key, MEMBERS_TTL, data)
		await delete_cache(self._members_key(chat_id))
		return member
