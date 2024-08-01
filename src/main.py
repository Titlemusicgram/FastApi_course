from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from src.operations.router import router as router_operation
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from src.auth.auth import auth_backend
from src.auth.models import User
from src.auth.router import router as auth_router
from src.tasks.router import router as tasks_router
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from redis import asyncio as aioredis

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="TradingApp", lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
app.include_router(auth_router)
app.include_router(tasks_router)
