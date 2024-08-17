import pytest
from fastapi.testclient import TestClient
from face_recognition_app.main import app
from face_recognition_app.app.utils.firebase_utils import add_to_firebase

client = TestClient(app)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module", autouse=True)
def setup_firebase():
    # Add initial test data to Firebase
    client_id = "123"
    data = {
        "name": "John Doe",
        "department": "Engineering",
        "type": "Visitor",
        "registered": "Added via Test",
        "last_recorded_time": "2023-01-01 00:00:00",
        "image_url": "http://example.com/test_image.jpg",
        "invited_by": "Jane Smith"
    }
    add_to_firebase(client_id, data)

def test_add_face(client):
    with open("image/schoolLogo.png", "rb") as file:
        response = client.post("/add_face", files={"file": file}, data={"client_id": "124", "name": "John Doe", "dept": "Engineering", "user_type": "Visitor", "invited_by": "Jane Smith"})
        print("add_face", response.json())
    assert response.status_code == 201
    assert response.json()["message"] == "Face added successfully"

def test_update_face(client):
    response = client.patch("/update_face", json={"client_id": "123", "name": "John Updated", "dept": "Research", "user_type": "Employee"})
    assert response.status_code == 200
    assert response.json()["message"] == "Client information updated successfully"

def test_get_users(client):
    response = client.get("/get_users")
    assert response.status_code == 200
    assert "users" in response.json()

def test_verify_face(client):
    with open("image/schoolLogo.png", "rb") as file:
        response = client.post("/verify_face", files={"file": file})
    if response.status_code == 200:
        assert response.json()["message"] == "Face verified"
    else:
        assert response.status_code == 404
        assert response.json()["message"] == "Face not recognized"

def test_delete_face(client):
    response = client.delete("/delete_face", params={"client_id": "123"})
    assert response.status_code == 200
    assert response.json()["message"] == "Client data deleted successfully"