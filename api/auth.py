"""
Authentication views (optional JWT).
"""

import os

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    JWT Login endpoint (optional).
    POST /api/v1/auth/login/
    """
    # Check if JWT is enabled
    enable_jwt = os.getenv("ENABLE_JWT", "False") == "True"
    if not enable_jwt:
        return Response(
            {"error": "JWT authentication is not enabled. Set ENABLE_JWT=True in .env"},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )

    try:
        from rest_framework_simplejwt.tokens import RefreshToken
    except ImportError:
        return Response(
            {"error": "JWT package not installed"}, status=status.HTTP_501_NOT_IMPLEMENTED
        )

    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(username=username)
        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    )
