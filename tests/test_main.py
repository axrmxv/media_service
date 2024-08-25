import os

from fastapi.testclient import TestClient
from app.main import main_router


client = TestClient(main_router)


def test_upload_file():
    file_path = "tests/test_files/test_image.jpg"
    with open(file_path, "rb") as file:
        response = client.post("/upload/", files={"file": file})

    assert response.status_code == 200
    data = response.json()
    assert "uid" in data
    assert os.path.exists(f"file_storage/{data['uid']}_test_image.jpg")


def test_get_file():
    file_path = "tests/test_files/test_image.jpg"
    with open(file_path, "rb") as file:
        response = client.post("/upload/", files={"file": file})

    assert response.status_code == 200
    uid = response.json()["uid"]

    response = client.get(f"/files/{uid}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


def test_file_not_found():
    response = client.get("/files/not_uid")
    assert response.status_code == 404
