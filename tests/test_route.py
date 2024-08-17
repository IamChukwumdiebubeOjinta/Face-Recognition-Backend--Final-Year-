from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_face():
    response = client.post('/add_face', json={
        "image": "<base64-encoded-image>",
        "name": "Test Name",
        "type": "Visitor",
        "invited_by": "Test Inviter"
    })
    assert response.status_code == 200
    assert response.json()['message'] == 'Face added successfully'
