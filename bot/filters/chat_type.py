from typing import Literal
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.enums.chat_type import ChatType

ValidChatType = Literal[ChatType.PRIVATE, ChatType.GROUP, ChatType.SUPERGROUP]

class ChatTypeFilter(BaseFilter):
	def __init__(self, chat_type: ValidChatType | list[ValidChatType]):
		self.chat_type = chat_type

	async def __call__(self, message: Message) -> bool:
		if isinstance(self.chat_type, str):
			return message.chat.type == self.chat_type
		else:
			return message.chat.type in self.chat_type
