from fastapi_users import FastAPIUsers
from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from fastapi import APIRouter, Depends


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

router = APIRouter()


@router.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@router.get("/unprotected-route")
def unprotected_route():
    return f"Hello, Anonym"
