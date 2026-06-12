class BotError(Exception):
	message = "❌ Error"

	def __str__(self):
		return self.message

	def log(self, event):
		return "Error"

class UserNotFoundError(BotError):
	message = "❌ User not found"

	def __init__(self, user_id_or_username: int | str):
		self.user_id_or_username = user_id_or_username

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"USER_NOT_FOUND | chat_id={chat_id} user_id={user_id} "
			f"target_id={self.user_id_or_username}"
		)

class NoUserInArgumentsError(BotError):
	message = "❌ User is missing"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"NO_USER_IN_ARGS | chat_id={chat_id} user_id={user_id}"

class DoubleUsernameInArgumentsError(BotError):
	message = "❌ Extra username in command"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"DOUBLE_USER_IN_ARGS | chat_id={chat_id} user_id={user_id}"

class InvalidUsernameOrIdInArgumentsError(BotError):
	message = "❌ Invalid username/ID"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"INVALID_USER_OR_ID | chat_id={chat_id} user_id={user_id}"

class TooManyArgumentsError(BotError):
	message = "❌ Too many arguments"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"TOO_MANY_ARGS | chat_id={chat_id} user_id={user_id}"

class MissingArgumentsError(BotError):
	message = "❌ Not enough arguments"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"MISSING_ARGS | chat_id={chat_id} user_id={user_id}"

class InvalidTimeArgumentError(BotError):
	message = "❌ Invalid time argument"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"INVALID_TIME_ARG | chat_id={chat_id} user_id={user_id}"

class CantChangeBotsRightsError(BotError):
	message = "❌ Cannot change rights of other bots"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"CANT_CHANGE_BOTS_RIGHTS | chat_id={chat_id} user_id={user_id}"
		)

class CantModerateAssignedNotByBotAdminsError(BotError):
	message = "❌ Cannot moderate admins not appointed by the bot"

	def __init__(self, target_id: int):
		self.target_id = target_id

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"CANT_MODERATE_ASSIGNED_NOT_BY_BOT_ADMINS | chat_id={chat_id} "
			f"user_id={user_id} target_id={self.target_id}"
		)

class AdminBotHasNoRightsError(BotError):
	message = "❌ Bot does not have enough rights"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)

		return f"BOT_HAS_NO_RIGHTS | chat_id={chat_id}"

class UserHasNoRightsError(BotError):
	message = "❌ You do not have enough rights"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"USER_HAS_NO_RIGHTS | chat_id={chat_id} user_id={user_id}"

class CantModerateAdminBotError(BotError):
	message = "❌ Cannot moderate the bot itself"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"CANT_MODERATE_BOT | chat_id={chat_id} user_id={user_id}"

class CantBanAdminError(BotError):
	message = "❌ Cannot ban administrators"

	def __init__(self, target_id: int):
		self.target_id = target_id

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"CANT_BAN_ADMIN | chat_id={chat_id} user_id={user_id} "
			f"target_id={self.target_id}"
		)

class UserNotBannedError(BotError): 
	message = "❌ User is not banned"

	def __init__(self, target_id: int):
		self.target_id = target_id

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"USER_NOT_BANNED | chat_id={chat_id} user_id={user_id} "
			f"target_id={self.target_id}"
		)

class CantMuteAdminError(BotError):
	message = "❌ Cannot mute administrators"

	def __init__(self, target_id: int):
		self.target_id = target_id

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"CANT_MUTE_ADMIN | chat_id={chat_id} user_id={user_id} "
			f"target_id={self.target_id}"
		)

class UserNotMutedError(BotError):
	message = "❌ User is not muted"

	def __init__(self, target_id: int):
		self.target_id = target_id

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"USER_NOT_MUTED | chat_id={chat_id} user_id={user_id} "
			f"target_id={self.target_id}"
		)

class CantKickAdminError(BotError):
	message = "❌ Cannot kick administrators"

	def __init__(self, target_id: int):
		self.target_id = target_id

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return (
			f"CANT_KICK_ADMIN | chat_id={chat_id} user_id={user_id} "
			f"target_id={self.target_id}"
		)

class KickMeAdminError(BotError):
	message = "❌ Remove your administrator rights to use this command"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"KICKME_ADMIN | chat_id={chat_id} user_id={user_id}"

class NeedReplyToMessageError(BotError):
	message = "❌ This command requires replying to a message"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"NEED_REPLY_TO_MESSAGE | chat_id={chat_id} user_id={user_id}"

class InvalidSettingModeError(BotError):
	message = "❌ Unknown setting mode"

	def log(self, event):
		chat_id = getattr(getattr(event, "chat", None), "id", None)
		user = getattr(event, "from_user", None)
		user_id = getattr(user, "id", None) if user else None

		return f"INVALID_SETTING_MODE | chat_id={chat_id} user_id={user_id}"
