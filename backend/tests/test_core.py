import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_me_requires_authentication():
    response = APIClient().get("/api/v1/auth/me/")
    assert response.status_code == 401

