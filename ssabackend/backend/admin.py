from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Event, Member, Family

# Register your models here.
class EventAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

class MemberAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

class FamilyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Family, FamilyAdmin)