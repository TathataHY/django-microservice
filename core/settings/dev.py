"""
Development settings for django-microservice project.
"""

from .base import *

DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Add debug toolbar in development (if available)
if DEBUG:
    try:
        import debug_toolbar

        INSTALLED_APPS += ["debug_toolbar"]
        MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
        INTERNAL_IPS = ["127.0.0.1", "localhost"]
    except ImportError:
        pass  # debug_toolbar not installed

# Less strict CORS in development
CORS_ALLOW_ALL_ORIGINS = True

# Show SQL queries in development
if DEBUG:
    LOGGING["loggers"]["django.db.backends"] = {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": False,
    }
