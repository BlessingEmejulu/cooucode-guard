import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/system/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["system"] == "COOUCodeGuard"

def test_auth_login():
    response = client.post("/api/auth/login", json={
        "email": "lecturer@coou.edu.ng",
        "password": "coouguard2026"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "lecturer@coou.edu.ng"

def test_dashboard_statistics():
    # Login first
    login_res = client.post("/api/auth/login", json={
        "email": "lecturer@coou.edu.ng",
        "password": "coouguard2026"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/dashboard/statistics", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "total_submissions" in data
    assert "total_scans" in data
    assert data["total_submissions"] >= 1

def test_courses_and_submissions():
    login_res = client.post("/api/auth/login", json={
        "email": "lecturer@coou.edu.ng",
        "password": "coouguard2026"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get courses
    c_res = client.get("/api/courses", headers=headers)
    assert c_res.status_code == 200
    courses = c_res.json()
    assert len(courses) >= 1

    # Get submissions
    s_res = client.get("/api/submissions", headers=headers)
    assert s_res.status_code == 200
    subs = s_res.json()
    assert len(subs) >= 1

def test_reports_endpoint():
    login_res = client.post("/api/auth/login", json={
        "email": "lecturer@coou.edu.ng",
        "password": "coouguard2026"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r_res = client.get("/api/reports", headers=headers)
    assert r_res.status_code == 200
    reports = r_res.json()
    assert len(reports) >= 1
