"""
Production settings for django-microservice project.
"""

import os

from .base import *

DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Security settings for production
# SECURE_SSL_REDIRECT defaults to True, but can be disabled for local testing
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() in ("true", "1", "yes")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = "DENY"

# Static files with WhiteNoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Database connection pooling
DATABASES["default"]["CONN_MAX_AGE"] = 600

# Logging in production (structured JSON)
# Override console formatter to use JSON
LOGGING["formatters"]["json"] = {
    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
    "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
}
LOGGING["handlers"]["console"]["formatter"] = "json"
