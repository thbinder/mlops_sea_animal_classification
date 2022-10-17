from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from src.api.app import app

client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong!"}

def test_predict_without_authentication():

    _test_upload_file = "./test_data/nudibranch.jpg"
    response = client.post(
        "/predict",
        files={"file": ("filename", open(_test_upload_file, "rb"), "image/jpeg")},
    )
    assert response.status_code == 401

def test_predict_with_authentication():

    _test_upload_file = "./test_data/nudibranch.jpg"
    auth = HTTPBasicAuth(username="thomas", password="thomas")
    response = client.post(
        "/predict",
        files={"file": ("filename", open(_test_upload_file, "rb"), "image/jpeg")},
        auth=auth
    )
    assert response.status_code == 200
