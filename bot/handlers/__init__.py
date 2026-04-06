
from aiogram import Router

from . import group, private

def get_routers() -> list[Router]:
	return [*group.routers, *private.routers]
