import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all('description' in v for v in data.values())

def test_signup_and_unregister():
    # Use a test email and activity
    test_email = "testuser@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))

    # Sign up
    signup = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert signup.status_code == 200
    assert "message" in signup.json()

    # Duplicate signup should fail
    signup2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert signup2.status_code == 400

    # Unregister
    unregister = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert unregister.status_code == 200
    assert "message" in unregister.json()

    # Unregister again should fail
    unregister2 = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert unregister2.status_code == 400
