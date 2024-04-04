from django.db import models
from django.contrib.auth.models import User
from gdstorage.storage import GoogleDriveStorage

gd_storage = GoogleDriveStorage()

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    participants = models.ManyToManyField(to="Member", related_name="events", blank=True)
    venue = models.TextField()
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True, upload_to="event_images", storage=gd_storage)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    family = models.ForeignKey(to="Family", on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    profile_image = models.ImageField(blank=True, null=True, upload_to="profile_images", storage=gd_storage)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True, blank=True)

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
