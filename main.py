from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from users.routers import router as users_router, auth_router as user_auth_router
from hotels.rooms.routers import router as rooms_router
from hotels.routers import router as hotels_router
from bookings.routers import router as bookings_router
from pages.routers import router as router_pages
from images.routers import router as image_router

app = FastAPI()

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
