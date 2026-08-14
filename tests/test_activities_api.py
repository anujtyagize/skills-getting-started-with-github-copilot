from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def reset_activities():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
    activities["Gym Class"]["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]


def test_get_activities_returns_activity_catalog():
    reset_activities()

    response = client.get("/activities")

    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    assert body["Chess Club"]["description"]
    assert len(body["Chess Club"]["participants"]) == 2


def test_signup_for_activity_adds_participant():
    reset_activities()
    email = "newstudent@mergington.edu"

    response = client.post("/activities/Chess Club/signup?email=" + email)

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_unknown_activity_returns_404():
    response = client.post("/activities/Unknown Club/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_student_returns_400():
    reset_activities()
    email = "michael@mergington.edu"

    response = client.post("/activities/Chess Club/signup?email=" + email)

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_them_from_activity():
    reset_activities()
    email = "daniel@mergington.edu"

    response = client.delete("/activities/Chess Club/participants?email=" + email)

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_404():
    reset_activities()
    email = "notregistered@mergington.edu"

    response = client.delete("/activities/Chess Club/participants?email=" + email)

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
