from .basic import router as basic_router
from .admin_func import router as admin_func_router
from .members import router as members_router

routers = [basic_router, admin_func_router, members_router]
