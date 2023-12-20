from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

from users.routers import router as users_router, auth_router as user_auth_router
from hotels.rooms.routers import router as rooms_router
from hotels.routers import router as hotels_router
from bookings.routers import router as bookings_router
from pages.routers import router as router_pages
from images.routers import router as image_router

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
    redis = aioredis.from_url("redis://localhost:6379")
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
