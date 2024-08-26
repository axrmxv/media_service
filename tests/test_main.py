import os
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import main_router
from fastapi import FastAPI


app = FastAPI()
app.include_router(main_router)


@pytest.fixture(scope="session")
def event_loop():
    """Создает и возвращает новый событийный цикл для тестов."""

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def test_client():
    """
    Создает и возвращает экземпляр AsyncClient для
    выполнения HTTP-запросов в тестах.
    """

    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_upload_file(test_client):
    """Тестирует загрузку файла через API и проверяет сохранение на сервере."""

    file_path = "tests/test_files/test_image.jpg"
    async with test_client as client:
        with open(file_path, "rb") as file:
            response = await client.post("/upload/", files={"file": file})

    assert response.status_code == 200
    data = response.json()
    assert "uid" in data
    assert os.path.exists(f"file_storage/{data['uid']}_test_image.jpg")


@pytest.mark.asyncio
async def test_get_file(test_client):
    """Тестирует получение файла по его UID и проверяет корректность ответа."""

    file_path = "tests/test_files/test_image.jpg"
    async with test_client as client:
        with open(file_path, "rb") as file:
            response = await client.post("/upload/", files={"file": file})

        assert response.status_code == 200
        uid = response.json()["uid"]

        response = await client.get(f"/files/{uid}")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/jpeg"


@pytest.mark.asyncio
async def test_file_not_found(test_client):
    """Тестирует сценарий, когда файл не найден по предоставленному UID."""

    uid = "not_uid"
    async with test_client as client:
        response = await client.get(f"/files/{uid}")
    assert response.status_code == 404
