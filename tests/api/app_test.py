from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong!"}


def test_predict():

    _test_upload_file = "./test_data/nudibranch.jpg"
    response = client.post(
        "/predict",
        files={"file": ("filename", open(_test_upload_file, "rb"), "image/jpeg")},
    )
    assert response.status_code == 200
