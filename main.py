from fastapi import FastAPI

from users.routers import router as users_router, auth_router as user_auth_router
from hotels.rooms.routers import router as rooms_router
from hotels.routers import router as hotels_router
from bookings.routers import router as bookings_router
from pages.routers import router as router_pages

# TODO: Создать дополнительные роуты
app = FastAPI()

app.include_router(user_auth_router)
app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(hotels_router)
app.include_router(bookings_router)
app.include_router(router_pages)


@app.get("/")
def read_root():
    return {"Hello": "World"}
