import shutil

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from tasks.tasks import process_pic

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"],
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    try:
        im_path = f"static/images/{name}.webp"
        with open(im_path, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        # Celery
        process_pic.delay(im_path)

        # Вернуть успешный ответ с кодом 201
        return JSONResponse(
            content={"message": "Фото успешно добавлено!"}, status_code=201
        )
    except Exception as e:
        # Обработать возможные ошибки и вернуть соответствующий ответ
        return JSONResponse(content={"message": f"Ошибка: {str(e)}"}, status_code=500)
