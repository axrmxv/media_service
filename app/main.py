import uvicorn

from fastapi import FastAPI
from fastapi.routing import APIRouter

from app.endpoints import upload_media, get_media
from cron.cron_task import start_scheduler


app = FastAPI(title="Media Service")


@app.get("/")
async def root():
    return {"message": "Hi"}

main_router = APIRouter()

main_router.include_router(upload_media, prefix="/upload")
main_router.include_router(get_media, prefix="/files")
app.include_router(main_router)


# Запускаем крон задачи при запуске приложения
start_scheduler()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
