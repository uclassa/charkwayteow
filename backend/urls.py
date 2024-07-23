from django.urls import include, path
from rest_framework import routers
from . import views as v

router = routers.SimpleRouter()
router.register(r"events", v.EventViewSet)
router.register(r"families", v.FamilyViewSet)
router.register(r"members/u", v.MemberUsernameViewSet, r"member-detail-username")
router.register(r"members/i", v.MemberIDViewset, r"member-detail-id")
router.register(r"submissions", v.PhotoSubmissionViewSet)

urlpatterns = [
    path("", include(router.urls))
]