import environ
from typing import Optional
from rest_framework import permissions

env = environ.Env(API_KEY=(str, None))


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission class to allow read-only access to non-admins
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff


class HasAPIAccess(permissions.BasePermission):
    """
    Permission class for sensitive endpoints,
    to lock it behind an API key.
    Key needs to be regenerated manually if compromised,
    server currently does not generate or store its own keys.
    """
    keyword = "api-key"

    def get_key(self, request) -> Optional[str]:
        """
        Get the API key from the request, if it exists
        """
        authorization = request.META.get("HTTP_AUTHORIZATION", "")

        if not authorization:
            return None

        keyword, found, key = authorization.partition(" ")
        if not found:
            return None

        if keyword.lower() != self.keyword.lower():
            return None

        return key

    def has_permission(self, request, view):
        return self.get_key(request) == env("API_KEY")
