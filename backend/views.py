from typing import Optional
from rest_framework import viewsets, permissions, mixins
from . import serializers as s, models as m

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


class EventViewSet(viewsets.ModelViewSet):
    """
    Event viewset. Read-only and participants are not visible for non-admins
    """
    queryset = m.Event.objects.filter(visible=True)
    # allow either IsAdminOrReadOnly or HasAPIAccess
    permission_classes = [IsAdminOrReadOnly | HasAPIAccess]
    serializer_class = s.EventPublicSerializer

    def get_serializer_class(self):
        if self.request.META.get("HTTP_AUTHORIZATION", None):
            return s.EventAPISerializer
        
        return super().get_serializer_class()


class FamilyViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    """
    Family viewset. Leaderboard only
    """
    queryset = m.Family.objects.all()
    serializer_class = s.FamilySerializer
    permission_classes = [HasAPIAccess]


class MemberUsernameViewSet(viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin):
    """
    Member viewset for telebot. Lookup using telegram handle.
    Case insensitive to accommodate for data entry inconsistencies.
    """
    queryset = m.Member.objects.all()
    serializer_class = s.MemberSerializer
    permission_classes = [HasAPIAccess]
    lookup_field = "telegram_username__iexact"


class MemberIDViewset(MemberUsernameViewSet):
    """
    Member viewset for telebot. Lookup using telegram id.
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


class GroupChatViewSet(viewsets.ModelViewSet):
    """
    Group chat viewset for telebot.
    """
    queryset = m.GroupChat.objects.all()
    serializer_class = s.GroupChatSerializer
    permission_classes = [HasAPIAccess]