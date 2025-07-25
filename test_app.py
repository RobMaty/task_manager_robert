import pytest
from app import app, db
from models import Task

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()


def test_home_get(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Task" in response.data


def test_add_task(client):
    response = client.post("/", data={
        "title": "Test Task",
        "description": "Test Description"
    }, follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        task = db.session.query(Task).filter_by(title="Test Task").first()
        assert task is not None
        assert task.description == "Test Description"


def test_edit_task(client):
    with app.app_context():
        task = Task(title="To Edit", description="Old")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.post("/edit_task", data={
        "task_id": task_id,
        "title": "Edited",
        "description": "New description"
    }, follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        updated = db.session.get(Task, task_id)
        assert updated.title == "Edited"
        assert updated.description == "New description"


def test_update_status(client):
    with app.app_context():
        task = Task(title="Status Test")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.post(f"/update_status/{task_id}", json={
        "status": "Done"
    })
    assert response.status_code == 200
    assert response.json["success"] is True

    with app.app_context():
        updated = db.session.get(Task, task_id)
        assert updated.status == "Done"


def test_delete_task(client):
    with app.app_context():
        task = Task(title="To Delete")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.get(f"/delete/{task_id}", follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        deleted = db.session.get(Task, task_id)
        assert deleted is None
