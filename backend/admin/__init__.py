from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionMixin
from .. import models as m
from . import resources as r, forms as f


@admin.display(description="Link to image")
def show_image_url(obj):
    """
    Function to display the image url as a clickable link in the admin panel
    """
    if obj.image_url:
        return format_html('<a href="{url}">image</a>', url=obj.image_url)
    return "No image"


@admin.display(description="Image preview")
def image_preview(obj):
    """
    Function to display the image as a hover preview
    """
    if obj.image_url:
        return format_html('<a href="javascript:void(0)" class="hover-preview" data-preview="{url}">image</a>', url=obj.image_url)
    return "No image"


class ImageFieldReorderedAdmin(admin.ModelAdmin):
    """
    Base admin class for the Event and Member models.
    Reorders the fields in the admin panel to have the image field at the bottom.
    NOTE: Since we're using google drive, any admin which includes the image field
    will be VERY SLOW (~1s) to load.
    """
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if image := form.base_fields.pop('image', None):
            form.base_fields['image'] = image
        if image_id := form.base_fields.pop('image_id', None):
            form.base_fields['image_id'] = image_id
        return form


@admin.register(m.Event)
class EventAdmin(ImportMixin, ExportActionMixin, ImageFieldReorderedAdmin):
    """
    Admin class for the Event model.
    Field order defined in the fields attribute.
    """
    resource_class = r.EventParticipantResource
    filter_horizontal = ('participants',)
    search_fields = ('title',)
    list_display = ('title', 'start_date', 'end_date', 'venue')
    readonly_fields = (show_image_url,)
    exclude = ('image_id',)


@admin.action(description="Mark selected members as inactive")
def make_inactive(modeladmin, request, queryset):
    """
    Admin action to mark members inactive
    """
    queryset.update(is_active=False)


@admin.register(m.Member)
class MemberAdmin(ImportExportMixin, admin.ModelAdmin):
    """
    Admin class for the Member model.
    Field order defined in the fields attribute.
    """
    resource_classes = (r.MemberResource,)
    search_fields = ('first_name', 'last_name')
    list_display = ('id', 'first_name', 'last_name', 'telegram_username', 'email', 'family')
    list_filter = ('is_active', 'is_admin', 'family')
    actions = (make_inactive,)


@admin.register(m.Family)
class FamilyAdmin(ImportExportMixin, admin.ModelAdmin):
    """
    Admin class for the Family model.
    """
    form = f.FamilyForm
    readonly_fields = ('points',)
    list_display = ('id', 'fam_name', 'points')


@admin.action(description="Mark selected submissions as vetted")
def make_vetted(modeladmin, request, queryset):
    """
    Admin action to mark submissions as vetted
    """
    queryset.update(vetted=True)


@admin.register(m.PhotoSubmission)
class PhotoSubmissionAdmin(ImportExportMixin, ImageFieldReorderedAdmin):
    """
    Admin class for the PhotoSubmission model.
    """
    class Media:
        js = [
            "backend/hoverImage.js"
        ]
        css = {
            "screen": ["backend/hover-image.css"]
        }

    list_display = ('id', 'date_uploaded', image_preview, 'member', 'family', 'description', 'number_of_people','score', 'vetted')
    list_filter = ('family', 'vetted', 'description')
    readonly_fields = (show_image_url,)
    exclude = ('image_id',)
    actions = (make_vetted,)


@admin.register(m.GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    """
    Admin class for the GroupChat model.
    """
    list_display = ('title', 'id')
