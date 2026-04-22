from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.mutable import MutableDict

class Base(DeclarativeBase):
	pass

class Member(Base):
	__tablename__ = "members"

	chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	username: Mapped[str | None] = mapped_column(String(64),
												 nullable=True, index=True)
	role: Mapped[str] = mapped_column(String(32), index=True)

	user_permissions: Mapped[dict] = mapped_column(
		MutableDict.as_mutable(JSONB),
		default=dict,
		server_default="{}"
	)
	admin_permissions: Mapped[dict] = mapped_column(
		MutableDict.as_mutable(JSONB),
		default=dict,
		server_default="{}"
	)

class BotChatInfo(Base):
	__tablename__ = "bot_chats_info"
	
	chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	chat_type: Mapped[str] = mapped_column(String(32), index=True)
	chat_username: Mapped[str | None] = mapped_column(String(64), \
													 nullable=True, index=True)
	bot_role: Mapped[str] = mapped_column(String(32), index=True)
	bot_user_permissions: Mapped[dict] = mapped_column(
		MutableDict.as_mutable(JSONB),
		default=dict,
		server_default="{}"
	)
	bot_admin_permissions: Mapped[dict] = mapped_column(
		MutableDict.as_mutable(JSONB),
		default=dict,
		server_default="{}"
	)
class ChatSettings(Base):
	__tablename__ = "chats_settings"

	chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	admin: Mapped[dict] = mapped_column(
		MutableDict.as_mutable(JSONB),
		default=dict,
		server_default="{}"
	)
