from rest_framework import viewsets, mixins, filters
from backend import serializers as s, models as m
from . import permissions as p
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timedelta
from django.conf import settings
from zoneinfo import ZoneInfo
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, SocialConnectView


class EventViewSetPagination(PageNumberPagination):
    """
    Pagination class to support pagination for telebot's /get_event_photodump command
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class EventViewSet(viewsets.ModelViewSet):
    """
    Event viewset. Behaviour is as follows:
    If an api key is not provided, uses the EventPublicSerializer and forbids unsafe methods. (this is for the website)
    If an api key is provided and is valid, uses the EventAPISerializer instead. (this is for the telebot)
    """
    queryset = m.Event.objects.filter(visible=True)
    permission_classes = [p.IsAdminOrReadOnly]
    serializer_class = s.EventPublicSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = '-start_date'
    pagination_class = EventViewSetPagination

    def get_permissions(self):
        if self.request.META.get("HTTP_AUTHORIZATION", None):
            # If the request has an auth header, we assume it wants to use the unsafe endpoint.
            return [p.HasAPIAccess()]

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
            one_year_ago = datetime.now(
                ZoneInfo(settings.TIME_ZONE)) - timedelta(days=365)
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
    permission_classes = [p.HasAPIAccess]


class MemberUsernameViewSet(viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin):
    """
    Member viewset for telebot. Lookup using telegram handle.
    Case insensitive to accommodate for data entry inconsistencies.
    """
    queryset = m.Member.objects.all()
    serializer_class = s.MemberSerializer
    permission_classes = [p.HasAPIAccess]
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
    permission_classes = [p.HasAPIAccess]


class GroupChatViewSet(viewsets.ModelViewSet):
    """
    Group chat viewset for telebot.
    """
    queryset = m.GroupChat.objects.all()
    serializer_class = s.GroupChatSerializer
    permission_classes = [p.HasAPIAccess]


class ExcoViewSet(viewsets.ModelViewSet):
    """
    Viewset for exco members
    """
    queryset = m.ExcoMember.objects.order_by("id")
    serializer_class = s.ExcoSerializer
    permission_classes = [p.IsAdminOrReadOnly]


class CompatibleOAuth2Client(OAuth2Client):
    """
    Workaround for dj-rest-auth incompatibility, omits the scope field from the constructor call
    """

    def __init__(
        self,
        request,
        consumer_key,
        consumer_secret,
        access_token_method,
        access_token_url,
        callback_url,
        scope,
        scope_delimiter=" ",
        headers=None,
        basic_auth=False,
    ):
        super().__init__(request, consumer_key, consumer_secret, access_token_method,
                         access_token_url, callback_url, scope_delimiter, headers, basic_auth)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.OAUTH_CALLBACK_URL
    client_class = CompatibleOAuth2Client


class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.OAUTH_CALLBACK_URL
    client_class = CompatibleOAuth2Client
