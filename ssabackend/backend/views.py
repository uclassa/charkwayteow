from rest_framework import viewsets, permissions, mixins
from . import serializers as s, models as m
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

    def _get_key(self, request) -> Optional[str]:
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
        return self._get_key(request) == env("API_KEY")


class EventViewSet(viewsets.ModelViewSet):
    """
    Event viewset. Read-only and participants are not visible for non-admins
    """
    queryset = m.Event.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        return s.EventSerializer if self.request.user.is_staff else s.EventPublicSerializer


class FamilyViewSet(viewsets.ModelViewSet):
    """
    Family viewset. Admin only
    TODO: Make this into a read only serializer without members for the telebot
    """
    queryset = m.Family.objects.all()
    serializer_class = s.FamilySerializer


class MemberUsernameViewSet(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin):
    """
    Member viewset for telebot. Lookup using telegram handle
    """
    queryset = m.Member.objects.all()
    serializer_class = s.MemberSerializer
    permission_classes = [HasAPIAccess]
    lookup_field = "telegram_username"

class MemberIDViewset(MemberUsernameViewSet):
    """
    Member viewset for telebot. Lookup using telegram id
    It's not easy to get the telegram id, so the id is updated automatically the first time the user uses the bot
    """
    lookup_field = "telegram_id"


class PhotoSubmissionViewSet(viewsets.GenericViewSet,
                             mixins.CreateModelMixin):
    """
    Photo submission viewset for telebot.
    """
    queryset = m.PhotoSubmission.objects.all()
    serializer_class = s.PhotoSubmissionSerializer
    permission_classes = [HasAPIAccess]
