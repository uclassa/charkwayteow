from rest_framework import viewsets, permissions
from backend.serializers import EventSerializer, EventPublicSerializer, FamilySerializer, MemberSerializer
from backend.models import Event, Family, Member
from typing import Optional

import environ
env = environ.Env(
    API_KEY=(str, None)
)


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
    Permission class to restrict access to the API to only those with the correct API key.
    Key needs to be regenerated manually if compromised.
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
        key = self.get_key(request)

        return key == env("API_KEY")


class EventViewSet(viewsets.ModelViewSet):
    """
    Event viewset. Read-only and participants are not visible for non-admins
    """
    queryset = Event.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        return EventSerializer if self.request.user.is_staff else EventPublicSerializer


class FamilyViewSet(viewsets.ModelViewSet):
    """
    Family viewset. Admin only
    TODO: Make this into a read only serializer without members for the telebot
    """
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [permissions.IsAdminUser]


class MemberViewSet(viewsets.ModelViewSet):
    """
    Member viewset. Admin only
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAdminUser]
