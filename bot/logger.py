import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_MODE = "compact"

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "bot.log"

def setup_logger():
	if LOG_MODE == "compact":
		console_formatter = logging.Formatter(
			"%(asctime)s | %(levelname)s | %(message)s",
		)
	elif LOG_MODE == "full":
		console_formatter = logging.Formatter(
			"%(asctime)s | %(levelname)s | "
			"%(name)s | %(funcName)s:%(lineno)d | %(message)s"
		)

	file_formatter = logging.Formatter(
		"%(asctime)s | %(levelname)s | "
		"%(name)s | %(funcName)s:%(lineno)d | %(message)s"
	)

	console_handler = logging.StreamHandler()
	console_handler.setFormatter(console_formatter)

	file_handler = RotatingFileHandler(
		LOG_FILE,
		maxBytes=10 * 1024 * 1024,
		backupCount=5,
		encoding="utf-8"
	)
	file_handler.setFormatter(file_formatter)

	root_logger = logging.getLogger()

	root_logger.handlers.clear()
	root_logger.setLevel(logging.INFO)

	root_logger.addHandler(console_handler)
	root_logger.addHandler(file_handler)
