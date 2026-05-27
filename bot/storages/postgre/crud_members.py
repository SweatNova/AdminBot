from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import TIMESTAMP
from datetime import datetime

from .models import Member

async def get_member_crud(session: AsyncSession, chat_id: int, user_id: int):
	return await session.get(Member, (chat_id, user_id))

async def get_member_by_username_crud(session: AsyncSession, chat_id: int,
									  username: str):
	result = await session.execute(
		select(Member).where(
			Member.chat_id == chat_id,
			Member.username == username
		)
	)
	return result.scalar_one_or_none()

async def get_members_crud(session: AsyncSession, chat_id: int):
	result = await session.execute(
		select(Member).where(Member.chat_id == chat_id)
	)
	return result.scalars().all()

async def create_member_crud(session: AsyncSession, chat_id: int, user_id: int,
							 username: str | None = None,
							 role: str | None = None,
							 user_permissions: dict | None = None,
							 admin_permissions: dict | None = None,
							 restricted_status: str | None = None,
							 admin_who_restricted: str | None = None,
							 start_time: TIMESTAMP | None = None,
							 end_time: TIMESTAMP | None = None) -> Member:
	member = Member(
		chat_id=chat_id,
		user_id=user_id,
		username=username,
		role=role,
		user_permissions = user_permissions,
		admin_permissions = admin_permissions,
		restricted_status = restricted_status,
		admin_who_restricted = admin_who_restricted,
		start_time = start_time,
		end_time = end_time
	)
	session.add(member)
	return member

async def delete_member_crud(session: AsyncSession, chat_id: int, user_id: int):
	await session.execute(
		delete(Member).where(
			Member.chat_id == chat_id,
			Member.user_id == user_id
		)
	)

async def get_punishments_crud(session, now: datetime):
	result = await session.execute(
		select(Member).where(
			(Member.end_time <= now)
		)
	)
	return result.scalars().all()
