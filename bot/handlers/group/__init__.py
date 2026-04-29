from .admin_func import router as admin_func_router
from .bans_func import router as bans_func_router
from .basic import router as basic_router
from .members import router as members_router

routers = [basic_router, admin_func_router, bans_func_router, members_router]
