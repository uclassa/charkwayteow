from django.contrib import admin
from django import forms
from import_export.admin import ImportExportModelAdmin
from . import models as m
from django.contrib.admin.widgets import FilteredSelectMultiple


class FamilyForm(forms.ModelForm):
    """
    Custom form for the Family model to allow for the selection of members
    """
    # Reverse relation to members
    members = forms.ModelMultipleChoiceField(
        queryset=m.Member.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Members',
            is_stacked=False
        )
    )

    class Meta:
        model = m.Family
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Override the init method to set the initial value of the members field to the current members of the family
        """
        super(FamilyForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['members'].initial = self.instance.members.all()

    def save(self, commit=True):
        """
        Override the save method to save the members to the family.
        Since the members are reverse relations, we need to set them manually.
        The function works as follows:
        1. Create the family instance by calling the parent save method
        2. Commit the instance to the database if commit is True
        3. Set the members of the family instance to the members selected in the form
        4. Save the many-to-many relationship
        5. Return the family instance
        """
        # Create the family instance.
        # Setting commit to False will not save the instance to the database, and creates the self.save_m2m() method to allow deferred saving of the m2m data
        family = super(FamilyForm, self).save(commit=False)

        if commit:
            family.save()

        if family.pk:
            family.members.set(self.cleaned_data['members'])
            self.save_m2m()

        return family


class EventAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Admin class for the Event model.
    Field order defined in the fields attribute.
    """
    filter_horizontal = ('participants',)
    search_fields = ('title',)
    list_display = ('title', 'start_date', 'end_date', 'venue')
    fields = ('title', 'start_date', 'end_date', 'venue', 'description', 'link', 'image', 'image_id', 'participants')


class MemberAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Admin class for the Member model.
    Field order defined in the fields attribute.
    """
    search_fields = ('name',)
    list_display = ('name', 'telegram_username', 'email', 'family')
    fields = ('name', 'dob', 'email', 'telegram_username', 'telegram_id', 'phone', 'gender', 'family', 'user', 'image', 'image_id')


class FamilyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Admin class for the Family model.
    """
    form = FamilyForm


class PhotoSubmissionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Admin class for the PhotoSubmission model.
    """
    list_display = ('date_uploaded', 'image', 'member', 'family', 'score')


admin.site.register(m.Event, EventAdmin)
admin.site.register(m.Member, MemberAdmin)
admin.site.register(m.Family, FamilyAdmin)
admin.site.register(m.PhotoSubmission, PhotoSubmissionAdmin)