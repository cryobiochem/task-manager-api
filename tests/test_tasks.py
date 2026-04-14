import pytest  # finds functions starting with test_ and runs them.
from fastapi.testclient import (
    TestClient,  # httpx library, lets you send real HTTP requests to FastAPI app
)

# without actually starting a server
from app.main import app, db


@pytest.fixture(autouse=True)  # Runs before every test
def clear_db():
    db.clear()  # Clear the in-memory database before
    # each test (Tests must be independent)
    yield  # hands control to the test function


client = TestClient(app)


# Verifies that when we create a task, we get a 201 status code and the
# correct response body. If this fails, it could mean the POST endpoint
# is broken or that the task isn't being saved correctly in the database.
def test_create_task_returns_201():
    response = client.post("/tasks", json={"title": "Buy milk"})
    assert (
        response.status_code == 201
    )  # 201 means "OK + I created something new with a POST request."
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["done"] is False
    assert "id" in data


# Verifies the clear_db fixture is working. If a previous test
# left data behind, this would catch it.
def test_list_tasks_empty_at_start():
    response = client.get("/tasks")
    assert (
        response.status_code == 200
    )  # 200 means "OK, I successfully processed your GET request."
    assert response.json() == []


# Verifies that when we create tasks, they show up in the list.
# If this fails, it could mean the POST or GET endpoints are broken,
# or that the clear_db fixture isn't working and tests are interfering with each other.
def test_list_tasks_returns_created_tasks():
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})
    response = client.get("/tasks")
    assert len(response.json()) == 2


# Verifies that when we mark a task as complete,
# its "done" status changes to True. If this fails,
# it could mean the PATCH endpoint is broken or that the task
# isn't being updated correctly in the database.
def test_complete_task_marks_done():
    create = client.post("/tasks", json={"title": "Do laundry"})
    task_id = create.json()["id"]
    response = client.patch(
        f"/tasks/{task_id}/complete"
    )  # PUT means "replace the entire resource." PATCH means "partially update it."
    assert response.status_code == 200
    assert response.json()["done"] is True


# Verifies that if we try to mark a non-existent task as complete,
# we get a 404 error. If this fails, it could mean the PATCH endpoint
# isn't properly checking if the task exists before trying to update it.
def test_complete_missing_task_returns_404():
    response = client.patch("/tasks/00000000-0000-0000-0000-000000000000/complete")
    assert response.status_code == 404


# Verifies that when we create a task, it uses a UUID for the ID. If this fails,
# it could mean the POST endpoint isn't generating IDs correctly.
def test_create_task_uses_uuid(mocker):
    fixed_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    mocker.patch("app.main.uuid4", return_value=fixed_id)
    response = client.post("/tasks", json={"title": "Mocked"})
    assert response.json()["id"] == fixed_id
