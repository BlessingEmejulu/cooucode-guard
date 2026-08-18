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

def test_student_login():
    response = client.post("/api/auth/login", json={
        "email": "student@coou.edu.ng",
        "password": "cooustudent2026"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "student@coou.edu.ng"
    assert data["user"]["role"] == "student"

def test_forgot_and_reset_password():
    # 1. Request recovery code
    req_res = client.post("/api/auth/forgot-password", json={
        "email": "lecturer@coou.edu.ng"
    })
    assert req_res.status_code == 200
    req_data = req_res.json()
    assert "reset_code" in req_data
    reset_code = req_data["reset_code"]

    # 2. Reset password
    reset_res = client.post("/api/auth/reset-password", json={
        "email": "lecturer@coou.edu.ng",
        "reset_code": reset_code,
        "new_password": "newcooupassword2026"
    })
    assert reset_res.status_code == 200

    # 3. Verify login with new password
    login_res = client.post("/api/auth/login", json={
        "email": "lecturer@coou.edu.ng",
        "password": "newcooupassword2026"
    })
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

    # 4. Restore original password
    client.post("/api/auth/reset-password", json={
        "email": "lecturer@coou.edu.ng",
        "reset_code": "COOU-ADMIN",
        "new_password": "coouguard2026"
    })

def test_dashboard_statistics():
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

    res = client.get("/api/reports", headers=headers)
    assert res.status_code == 200
    reports = res.json()
    assert isinstance(reports, list)
