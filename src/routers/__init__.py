from fastapi import APIRouter
from src.routers.auth import router as auth
from src.routers.supervisor import router as supervisor
from src.routers.user import router as user

router = APIRouter(prefix="/api")
router.include_router(auth, prefix="/auth", tags=["Authorization"])
router.include_router(supervisor, prefix="/supervisor", tags=["Supervisor"])
router.include_router(user, prefix="/user", tags=["User"])
