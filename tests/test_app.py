import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Make sure not already signed up
    client.get("/activities")  # warm up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Check participant added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_for_activity_already_signed_up():
    email = "michael@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_signup_for_activity_not_found():
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant():
    # Add then remove
    email = "removeme@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Simulate DELETE endpoint
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Should fail (endpoint not implemented yet)
    assert response.status_code in (404, 405)
