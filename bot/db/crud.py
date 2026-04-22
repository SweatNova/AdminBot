from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Member

async def upsert_member(session: AsyncSession, chat_id: int, user_id: int,
						username: str | None, role: str,
						user_permissions: dict | None,
						admin_permissions: dict | None) -> Member:
	member = await get_member(session, chat_id, user_id)
	if member:
		member.username = username
		member.role = role
		member.user_permissions = user_permissions
		member.admin_permissions = admin_permissions
	else:
		await update_member(session, chat_id, user_id, username, role,
							user_permissions, admin_permissions)
	return member

async def update_member(session: AsyncSession, chat_id: int, user_id: int,
						username: str | None, role: str,
						user_permissions: dict | None,
						admin_permissions: dict | None) -> None:
	member = Member(
		chat_id=chat_id,
		user_id=user_id,
		username=username,
		role=role,
		user_permissions = user_permissions,
		admin_permissions = admin_permissions
	)
	session.add(member)

async def get_member(session: AsyncSession, chat_id: int, user_id: int):
	return await session.get(Member, (chat_id, user_id))

async def get_members(session: AsyncSession, chat_id: int):
	result = await session.execute(
		select(Member).where(Member.chat_id == chat_id)
	)
	return result.scalars().all()

async def get_member_by_username(session: AsyncSession, chat_id: int,
                                 username: str):
	result = await session.execute(
		select(Member).where(
			Member.chat_id == chat_id,
			Member.username == username
		)
	)
	return result.scalar_one_or_none()

async def delete_member(session: AsyncSession, chat_id: int, user_id: int):
	await session.execute(
		delete(Member).where(
			Member.chat_id == chat_id,
			Member.user_id == user_id
		)
	)
