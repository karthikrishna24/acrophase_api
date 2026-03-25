from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


# Base payload
def valid_payload(session_id="test_sess_1"):
    return {
        "session_id": session_id,
        "user_id": 1,
        "workout_name": "run",
        "workout_type": "cardio",
        "calories_burned": 200,
        "start_time": "2026-03-24T06:00:00Z",
        "end_time": "2026-03-24T06:30:00Z",
    }


# 1. Valid input
def test_valid_input():
    res = client.post("/webhook/session", json=valid_payload("valid_1"))
    assert res.status_code == 201
    assert "successfully" in res.json()["message"]


# 2. Invalid input (wrong type)
def test_invalid_input():
    payload = valid_payload("invalid_1")
    payload["calories_burned"] = "wrong_type"

    res = client.post("/webhook/session", json=payload)
    assert res.status_code == 422  # validation error


# 3. Duplicate check
def test_duplicate_session():
    payload = valid_payload("dup_1")

    client.post("/webhook/session", json=payload)
    res = client.post("/webhook/session", json=payload)

    assert res.status_code == 200
    assert "already exists" in res.json()["message"]


# 4. end_time < start_time
def test_invalid_time():
    payload = valid_payload("time_err_1")
    payload["end_time"] = "2026-03-24T05:00:00Z"

    res = client.post("/webhook/session", json=payload)
    assert res.status_code == 422


# 5. Missing field
def test_missing_field():
    payload = valid_payload("missing_1")
    del payload["user_id"]

    res = client.post("/webhook/session", json=payload)
    assert res.status_code == 422


# 6. Bulk insert (simulate CSV data)
def test_bulk_insert():
    for i in range(5):
        payload = valid_payload(f"bulk_{i}")
        res = client.post("/webhook/session", json=payload)
        assert res.status_code == 201


# 7. Pagination test
def test_pagination():
    # Insert dummy data
    for i in range(10):
        payload = valid_payload(f"page_{i}")
        client.post("/webhook/session", json=payload)

    res = client.get("/sessions?user_id=1&limit=5&offset=0")

    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) <= 5
