from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_courses():
    response = client.get("/courses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_course_overview():
    response = client.get("/courses/{valid_course_id}")
    assert response.status_code == 200
    assert "name" in response.json()

def test_get_chapter_info():
    response = client.get("/courses/{valid_course_id}/chapters/{valid_chapter_id}")
    assert response.status_code == 200
    assert "name" in response.json()

def test_rate_chapter():
    response = client.post("/courses/{valid_course_id}/chapters/{valid_chapter_id}/rate", json={"rating": 1})
    assert response.status_code == 200
    assert response.json()["message"] == "Rating submitted successfully"
