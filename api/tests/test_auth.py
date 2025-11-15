"""
Tests for authentication endpoints.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """Create API client."""
    return APIClient()


@pytest.fixture
def test_user():
    """Create a test user."""
    return User.objects.create_user(
        username="testuser", password="testpass123", email="test@example.com"
    )


@pytest.mark.django_db
class TestJWTAuth:
    """Tests for JWT authentication."""

    def test_login_success(self, api_client, test_user):
        """Test successful login."""
        url = reverse("auth-login")
        data = {"username": "testuser", "password": "testpass123"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["access"] is not None
        assert response.data["refresh"] is not None

    def test_login_invalid_credentials(self, api_client, test_user):
        """Test login with invalid credentials."""
        url = reverse("auth-login")
        data = {"username": "testuser", "password": "wrongpassword"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "error" in response.data

    def test_login_missing_credentials(self, api_client):
        """Test login with missing credentials."""
        url = reverse("auth-login")
        data = {}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_login_nonexistent_user(self, api_client):
        """Test login with non-existent user."""
        url = reverse("auth-login")
        data = {"username": "nonexistent", "password": "password"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "error" in response.data

    # Note: Tests for JWT not enabled and package not installed are complex
    # because they require module reloading. These edge cases are covered
    # by the code structure but are difficult to test without affecting
    # other tests. The main authentication flow is tested above.