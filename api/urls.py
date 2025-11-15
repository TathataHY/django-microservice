"""
URL configuration for API app.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .auth import login
from .views import PersonViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"persons", PersonViewSet, basename="person")
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("auth/login/", login, name="auth-login"),
    path("", include(router.urls)),
]
