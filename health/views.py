"""
Health check and metrics views.
"""

import logging

from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

logger = logging.getLogger(__name__)

# Prometheus metrics
http_requests_total = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds", "HTTP request duration in seconds", ["method", "endpoint"]
)


@require_http_methods(["GET"])
def healthz(request):
    """
    Health check endpoint - checks if the application is alive.
    GET /healthz
    """
    return JsonResponse({"status": "ok", "service": "django-microservice"})


@require_http_methods(["GET"])
def readyz(request):
    """
    Readiness check endpoint - checks if the database is connected.
    GET /readyz
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return JsonResponse({"status": "ready", "database": "connected"})
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return JsonResponse(
            {"status": "not ready", "database": "disconnected", "error": str(e)}, status=503
        )


@require_http_methods(["GET"])
def metrics(request):
    """
    Prometheus metrics endpoint.
    GET /metrics
    """
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
