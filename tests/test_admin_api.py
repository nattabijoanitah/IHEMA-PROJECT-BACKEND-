import pytest

from app import create_app
from app.extensions import db
from app.models.rbac import User, Role
from app.models.page import Page


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with app.app_context():
        db.drop_all()
        db.create_all()
        role = Role(name="admin")
        db.session.add(role)
        db.session.commit()
        user = User(full_name="Admin", email="admin@example.com", role=role)
        user.set_password("secret")
        db.session.add(user)
        db.session.commit()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_dashboard_requires_admin(client):
    response = client.get("/api/admin/dashboard")
    assert response.status_code == 401


def test_dashboard_returns_counts(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "secret"},
    )
    token = response.get_json()["access_token"]

    response = client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["total_users"] >= 1
    assert payload["total_sermons"] == 0
