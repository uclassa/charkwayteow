from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .. import models as m


class ModdedFilteredSelectMultiple(FilteredSelectMultiple):
    """
    Modified widget for the family form. Fixes problem with the members label being after the widget.
    Changed 1 line inside the static js file...
    """
    class Media:
        extend = False
        js = [
            "admin/js/core.js",
            "admin/js/SelectBox.js",
            "backend/SelectFilter3.js", # this is the custom js file
        ]


class FamilyForm(forms.ModelForm):
    """
    Custom form for the Family model to allow for the selection of members
    """
    # Reverse relation to members
    members = forms.ModelMultipleChoiceField(
        queryset=m.Member.objects.all(),
        required=False,
        widget=ModdedFilteredSelectMultiple(
            verbose_name='Members',
            is_stacked=False
        ),
    )

    class Meta:
        model = m.Family
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Overridden init method.
        Sets the initial value of the members field to the current members of the family.
        """
        super().__init__(*args, **kwargs)

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
        # Setting commit to False will not save the instance to the database immediately
        # but instead creates the self.save_m2m() method to allow deferred saving of the m2m data
        family = super().save(commit=False)

        if commit:
            family.save()

        if family.pk:
            family.members.set(self.cleaned_data['members'])
            self.save_m2m()

        return family
