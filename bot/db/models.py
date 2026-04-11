from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, BigInteger

class Base(DeclarativeBase):
    pass

class Member(Base):
    __tablename__ = "members"

    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    username: Mapped[str | None] = mapped_column(String(64), index=True)
    role: Mapped[str] = mapped_column(String(64))
