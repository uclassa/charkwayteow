from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from . import views as v
from dj_rest_auth.registration.views import SocialAccountListView, SocialAccountDisconnectView

router = routers.SimpleRouter()
router.register(r"events", v.EventViewSet)
router.register(r"families", v.FamilyViewSet)
router.register(r"members/u", v.MemberUsernameViewSet,
                r"member-detail-username")
router.register(r"members/i", v.MemberIDViewset, r"member-detail-id")
router.register(r"submissions", v.PhotoSubmissionViewSet)
router.register(r"chats", v.GroupChatViewSet)
router.register(r"exco", v.ExcoViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('dj-rest-auth/google/', v.GoogleLogin.as_view(),
         name='google_login'),
    path('dj-rest-auth/google/connect',
         v.GoogleConnect.as_view(), name='google_connect'),
    path(
        'socialaccounts/',
        SocialAccountListView.as_view(),
        name='social_account_list'
    ),
    path(
        'socialaccounts/<int:pk>/disconnect/',
        SocialAccountDisconnectView.as_view(),
        name='social_account_disconnect'
    ),
    path(
        'accounts/google/login/token/',
        csrf_exempt(v.GoogleLoginByTokenView.as_view()),
        name='google_login_by_token'
    )
]
