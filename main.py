import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView

from admin.auth import authentication_backend
from admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin

from users.routers import router as users_router, auth_router as user_auth_router
from hotels.rooms.routers import router as rooms_router
from hotels.routers import router as hotels_router
from bookings.routers import router as bookings_router
from pages.routers import router as router_pages
from images.routers import router as image_router
from users.models import Users
from config import settings
from database import engine


app = FastAPI()


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


app.mount("/static", StaticFiles(directory="static"), "static")

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


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
