from django.contrib import admin
from django import forms
from import_export.admin import ImportExportModelAdmin
from .models import Event, Member, Family
from django.contrib.admin.widgets import FilteredSelectMultiple

# Register your models here.
class FamilyForm(forms.ModelForm):
    # Reverse relation to members
    members = forms.ModelMultipleChoiceField(
        queryset=Member.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Members',
            is_stacked=False
        )
    )

    class Meta:
        model = Family
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(FamilyForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['members'].initial = self.instance.members.all()
    
    def save(self, commit=True):
        family = super(FamilyForm, self).save(commit=False)

        if commit:
            family.save()

        if family.pk:
            family.members.set(self.cleaned_data['members'])
            self.save_m2m()
        
        return family


class EventAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    filter_horizontal = ('participants',)
    search_fields = ('title',)
    list_display = ('title', 'start_date', 'end_date', 'venue')


class MemberAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'email', 'family')


class FamilyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = FamilyForm


admin.site.register(Event, EventAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Family, FamilyAdmin)