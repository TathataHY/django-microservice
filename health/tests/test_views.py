"""
Tests for health check views.
"""

import pytest
from django.test import Client


@pytest.mark.django_db
class TestHealthViews:
    """Tests for health check endpoints."""

    def test_healthz(self):
        """Test healthz endpoint."""
        client = Client()
        response = client.get("/healthz/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "django-microservice"

    def test_readyz_with_db(self):
        """Test readyz endpoint with database connection."""
        client = Client()
        response = client.get("/readyz/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["database"] == "connected"

    def test_metrics(self):
        """Test metrics endpoint."""
        client = Client()
        response = client.get("/metrics/")
        assert response.status_code == 200
        assert "text/plain" in response["Content-Type"]
        assert b"http_requests_total" in response.content
