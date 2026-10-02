import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User


@pytest.mark.django_db
def test_register_and_login():
    client = APIClient()
    response = client.post("/api/v1/auth/register/", {"email": "user@example.com", "password": "Strong-password-123"})
    assert response.status_code == 201
    assert User.objects.filter(email="user@example.com").exists()
    response = client.post("/api/v1/auth/login/", {"email": "user@example.com", "password": "Strong-password-123"})
    assert response.status_code == 200
    assert "access" in response.data

