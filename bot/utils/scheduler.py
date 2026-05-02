import asyncio
from datetime import datetime

from bot.db import get_session
from bot.db.crud_members import get_punishments, upsert_punishments

async def punishments_worker(bot):
    while True:
        async with get_session() as session:
            users = await get_punishments(session, datetime.utcnow())
            for user in users:
                try:
                    if user.restricted_status == "banned":
                        await bot.unban_chat_member(user.chat_id, user.user_id)
                    elif user.restricted_status == "muted":
                        await bot.restrict_chat_member(
                            user.chat_id,
                            user.user_id,
                            permissions={
                                "can_send_messages": True,
                            }
                        )

                    await upsert_punishments(session, user.chat_id,
											 user.user_id, None, None,
											 None, None)
                except Exception as e:
                    print(f"Ошибка при снятии наказания: {e}")
        await asyncio.sleep(5)
