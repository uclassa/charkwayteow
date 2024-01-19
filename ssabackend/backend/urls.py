from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r"events", views.EventViewSet)
router.register(r"family", views.FamilyViewSet)
router.register(r"member", views.MemberViewSet)

urlpatterns = [
    path("", include(router.urls))
]