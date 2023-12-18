from fastapi import FastAPI

from users.routers import router as users_router, auth_router as user_auth_router
from rooms.routers import router as rooms_router
from hotels.routers import router as hotels_router
from bookings.routers import router as bookings_router

# TODO: Создать дополнительные роуты
app = FastAPI()

app.include_router(user_auth_router)
app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(hotels_router)
app.include_router(bookings_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
