from fastapi import APIRouter, UploadFile
import shutil

from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"],
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    try:
        with open(f"static/images/{name}.webp", "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        # Вернуть успешный ответ с кодом 201
        return JSONResponse(
            content={"message": "Фото успешно добавлено!"}, status_code=201
        )
    except Exception as e:
        # Обработать возможные ошибки и вернуть соответствующий ответ
        return JSONResponse(content={"message": f"Ошибка: {str(e)}"}, status_code=500)
