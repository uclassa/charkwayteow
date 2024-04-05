from django.db import models
from django.contrib.auth.models import User
from .drive import ModifiedGoogleDriveStorage

gd_storage = ModifiedGoogleDriveStorage()    

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    participants = models.ManyToManyField(to="Member", related_name="events", blank=True)
    venue = models.TextField()
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="event_images", storage=gd_storage)
    link = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check if the instance is being updated
        if self.pk:
            try:
                # Retrieve the previous value of the image field
                prev_instance = Event.objects.get(pk=self.pk)
                prev_image = prev_instance.image
            except Event.DoesNotExist:
                prev_image = None

        # Call the parent class's save method
        super().save(*args, **kwargs)

        # Check if the image field has been updated or cleared
        if self.image != prev_image:
            if self.image:
                # Generate the URL of the image based on its path
                # Update the image_url field with the URL
                self.image_url = self.image.url
            else:
                # If the image field has been cleared, clear the image_url field as well
                self.image_url = None
            # Save the model again to update the image_url field
            super().save(update_fields=['image_url'])


    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    family = models.ForeignKey(to="Family", on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    profile_image_url = models.URLField(blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to="profile_images", storage=gd_storage)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if the instance is being updated
        if self.pk:
            try:
                # Retrieve the previous value of the image field
                prev_instance = Member.objects.get(pk=self.pk)
                prev_image = prev_instance.image
            except Member.DoesNotExist:
                prev_image = None

        # Call the parent class's save method
        super().save(*args, **kwargs)

        # Check if the image field has been updated or cleared
        if self.image != prev_image:
            if self.image:
                # Generate the URL of the image based on its path
                # Update the image_url field with the URL
                self.profile_image_url = self.image.url
            else:
                # If the image field has been cleared, clear the image_url field as well
                self.image_url = None
            # Save the model again to update the image_url field
            super().save(update_fields=['profile_image_url'])

    def __str__(self):
        return self.name

class Family(models.Model):
    fam_name = models.CharField(max_length=30)
    points = models.IntegerField(default=0)
    # score_log = models.ForeignKey(to="ScoreLog")

    def __str__(self):
        return self.fam_name

# class ScoreLog(models.Model):
#     date_uploaded = models.DateTimeField()
#     result = models.TextField()
#     score = models.IntegerField()
