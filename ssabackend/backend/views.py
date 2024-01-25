from rest_framework import viewsets, permissions
from backend.serializers import EventSerializer, EventPublicSerializer, FamilySerializer, MemberSerializer
from backend.models import Event, Family, Member

# Create your views here.

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff


# Event is read-only for non-admins
# Participants invisible to non-admins
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        return EventSerializer if self.request.user.is_staff else EventPublicSerializer


# Only admins can view families and list members
class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [permissions.IsAdminUser]


# User has only permission for their own member object
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAdminUser]


"""
TODO: 
- Endpoints for user rsvp to event (add/remove me from event)
- me endpoint (get user and related profile info, update profile info)
- creating user and associate with member on first login
"""