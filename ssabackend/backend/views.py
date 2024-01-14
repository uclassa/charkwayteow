from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Event

# Create your views here.
def index(request):
    return HttpResponse("Hello world")

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()