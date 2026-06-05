class BotError(Exception):
	message = "❌ Ошибка"

	def __str__(self):
		return self.message

	def log(self, event):
		return "Error"

class UserNotFoundError(BotError):
	message = "❌ Юзер не найден"

	def __init__(self, user_id_or_username: int | str):
		self.user_id_or_username = user_id_or_username

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"in chat {chat_id} user {user_id} write "
			f"unknown user {self.user_id_or_username}"
		)

class NoUserInArgumentsError(BotError):
	message = "❌ Oтсутствует юзер"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"in chat {chat_id} user {user_id} missing username argument"

class DoubleUsernameInArgumentsError(BotError):
	message = "❌ Лишний юзернейм в команде"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"in chat {chat_id} user {user_id} write "
			"double username in arguments"
		)

class InvalidUsernameOrIdInArgumentsError(BotError):
	message = "❌ Некорректный юзернейм/айди"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"in chat {chat_id} user {user_id} write invalid username or id"

class TooManyArgumentsError(BotError):
	message = "❌ Слишком много аргументов"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"in chat {chat_id} user {user_id} write too many arguments"

class MissingArgumentsError(BotError):
	message = "❌ Недостаточно аргументов"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"in chat {chat_id} user {user_id} missing arguments"

class InvalidTimeArgumentError(BotError):
	message = "❌ Некорректный временной аргумент"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"in chat {chat_id} user {user_id} write invalid time argument"

class CantChangeBotsRightsError(BotError):
	message = "❌ Бот не может менять права другим ботам"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"in chat {chat_id} user {user_id} tried to change "
			"another bot rights"
		)

class CantModerateAssignedNotByBotAdminsError(BotError):
	message = "❌ Бот не может модерировать админов назначенных не им"

	def __init__(self, admin_id: int):
		self.admin_id = admin_id

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"in chat {chat_id} user {user_id} tried to moderate "
			f"assigned not by AdminBot admin {self.admin_id}"
		)

class AdminBotHasNoRightsError(BotError):
	message = "❌ У бота недостаточно прав"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)

		return f"in chat {chat_id} AdminBot doesn't have enough rights"

class UserHasNoRightsError(BotError):
	message = "❌ У вас недостаточно прав"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"in chat {chat_id} user {user_id} doesn't have enough rights"

class CantModerateAdminBotError(BotError):
	message = "❌ Нельзя модерировать самого бота"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"in chat {chat_id} user {user_id} tried to moderate AdminBot"

class CantBanAdminError(BotError):
	message = "❌ Нельзя банить админов"

	def __init__(self, admin_id: int):
		self.admin_id = admin_id

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"in chat {chat_id} user {user_id} "
			f"tried to ban admin {self.admin_id}"
		)

class UserNotBannedError(BotError): 
	message = "❌ Юзер не в бане"

	def __init__(self, victim_id: int):
		self.victim_id = victim_id

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"in chat {chat_id} user {user_id} tried to unban "
			f"not banned user {self.victim_id}"
		)

class CantMuteAdminError(BotError):
	message = "❌ Нельзя мутить админов"

	def __init__(self, admin_id: int):
		self.admin_id = admin_id

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"in chat {chat_id} user {user_id} "
			f"tried to mute admin {self.admin_id}"
		)

class UserNotMutedError(BotError):
	message = "❌ Юзер не в муте"

	def __init__(self, victim_id: int):
		self.victim_id = victim_id

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"in chat {chat_id} user {user_id} tried to unmute "
			f"not muted user {self.victim_id}"
		)

class CantKickAdminError(BotError):
	message = "❌ Нельзя кикать админов"

	def __init__(self, admin_id: int):
		self.admin_id = admin_id

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"in chat {chat_id} user {user_id} "
			f"tried to kick admin {self.admin_id}"
		)

class KickMeAdminError(BotError):
	message = "❌ Лишите себя прав администратора для выполнения команды"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"in chat {chat_id} user {user_id} tried kickme but is admin"

class NeedReplyToMessageError(BotError):
	message = "❌ Команде требуется реплай на сообщениe"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"in chat {chat_id} user {user_id} missing reply"

class InvalidSettingModeError(BotError):
	message = "❌ Неизвестный режим настройки"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"in chat {chat_id} user {user_id} write invalid setting mode"
