from django.utils.encoding import force_str
from import_export import resources
from .. import models as m


class EventParticipantResource(resources.ModelResource):
    """
    Resource class for exporting participant data for events.
    Note that the metaclass uses the `Member` model since it's member data that we are exporting.
    """
    class Meta:
        model = m.Member
        # TODO: update this accordingly with member model changes
        fields = ('first_name', 'last_name', 'dob', 'email', 'telegram_username')

    def get_export_headers(self, selected_fields=None):
        """
        Override get_export_headers so that the headers for the exported file are human friendly.
        """
        export_fields = self.get_export_fields(selected_fields)
        export_headers = [force_str(field.column_name) for field in export_fields if field]
        return [header.replace("_", " ").capitalize() for header in export_headers]

    def export(self, queryset=None, **kwargs):
        """
        Override export method to export the linked participants instead of the event itself.
        Will only export linked participants for the first event in the queryset.
        It only makes sense to export participants for a single event anyway.
        """
        if queryset is None:
            return None

        return super().export(queryset.first().participants.all(), **kwargs)


class MemberResource(resources.ModelResource):
    """
    Resource for member model.
    """
    class Meta:
        model = m.Member
        import_id_fields = ("id",)
