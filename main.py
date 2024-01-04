import time
import uvicorn
import sentry_sdk
from config import settings
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView

from admin.auth import authentication_backend
from admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from bookings.routers import router as bookings_router
from config import settings
from database import engine
from hotels.rooms.routers import router as rooms_router
from hotels.routers import router as hotels_router
from images.routers import router as image_router
from pages.routers import router as router_pages
from logger import logger
from users.routers import auth_router as user_auth_router
from users.routers import router as users_router

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = FastAPI()


# @app.get("/sentry-debug")
# async def trigger_error():
#     exc = 2 + "str"


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control_Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.on_event("startup")  # <-- данный декоратор прогоняет код перед запуском FastAPI
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")


# Подключение версионирования
app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/api/v{major}",
)

## Логгер времени исполнения запроса:
# @app.middleware("http")
# async def time_logger(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     logger.info("Request handling time", extra={"process time": round(process_time, 4)})
#     return response


app.include_router(user_auth_router)
app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(hotels_router)
app.include_router(bookings_router)
app.include_router(router_pages)
app.include_router(image_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)


app.mount("/static", StaticFiles(directory="static"), "static")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
