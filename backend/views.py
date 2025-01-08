from typing import Optional
from rest_framework import viewsets, permissions, mixins, filters
from . import serializers as s, models as m
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timedelta
from django.conf import settings
from zoneinfo import ZoneInfo

import environ

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


class EventViewSetPagination(PageNumberPagination):
    """
    Pagination class to support pagination for telebot's /get_event_photodump command
    """
    page_size = 4
    page_size_query_param = "page_size"
    max_page_size = 5


class EventViewSet(viewsets.ModelViewSet):
    """
    Event viewset. Behaviour is as follows:
    If an api key is not provided, uses the EventPublicSerializer and forbids unsafe methods. (this is for the website)
    If an api key is provided and is valid, uses the EventAPISerializer instead. (this is for the telebot)
    """
    queryset = m.Event.objects.filter(visible=True)
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = s.EventPublicSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = 'start_date'
    pagination_class = EventViewSetPagination

    def get_permissions(self):
        if self.request.META.get("HTTP_AUTHORIZATION", None):
            # If the request has an auth header, we assume it wants to use the unsafe endpoint.
            return [HasAPIAccess()]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.META.get("HTTP_AUTHORIZATION", None):
            return s.EventAPISerializer

        return super().get_serializer_class()
    
    # conditionally paginate the queryset, if the unsafe endpoint is used
    def paginate_queryset(self, queryset):
        if self.request.META.get("HTTP_AUTHORIZATION", None):
            return super().paginate_queryset(queryset)
        return None
    
    # only return events that have occured in the past year if the unsafe endpoint is used
    def get_queryset(self):
        if self.request.META.get("HTTP_AUTHORIZATION", None):
            one_year_ago = datetime.now(ZoneInfo(settings.TIME_ZONE)) - timedelta(days=365)
            today = datetime.now(ZoneInfo(settings.TIME_ZONE))

            # filtering for events that happend less than a year ago, since there cannot be photos for an event that has not happened yet
            return m.Event.objects.filter(visible=True, start_date__gte=one_year_ago, start_date__lte=today)
        return super().get_queryset()


class FamilyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
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


class PhotoSubmissionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
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


class ExcoViewSet(viewsets.ModelViewSet):
    """
    Viewset for exco members
    """
    queryset = m.ExcoMember.objects.all()
    serializer_class = s.ExcoSerializer
    permission_classes = [IsAdminOrReadOnly]
