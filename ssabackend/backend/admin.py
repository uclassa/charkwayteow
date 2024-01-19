from django.contrib import admin
from .models import Event, Member, Family

# Register your models here.
admin.site.register(Event)
admin.site.register(Member)
admin.site.register(Family)