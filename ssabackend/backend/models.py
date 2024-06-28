from django.db import models
from django.contrib.auth.models import User
from gdstorage.storage import GoogleDriveStorage

gd_storage = GoogleDriveStorage()

def get_image_id(url):
    suffix = '&export=download'
    prefix = 'id='
    
    start_idx = url.find(prefix)
    if start_idx is None:
        start_idx = 0
    else:
        start_idx += len(prefix)
    
    end_idx = url.find(suffix)
    if end_idx is None:
        end_idx = len(id)
    
    return url[start_idx:end_idx]

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    participants = models.ManyToManyField(to="Member", related_name="events", blank=True)
    venue = models.TextField()
    description = models.TextField(blank=True)
    image_id = models.CharField(blank=True, null=True, verbose_name="Image id (do not edit)")
    image = models.ImageField(blank=True, null=True, upload_to="event_images", storage=gd_storage)
    link = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        try: # Check if the instance is being updated
            prev_image = Event.objects.get(pk=self.pk).image
        except Event.DoesNotExist: # If the instance is being created, set the previous image to None
            prev_image = None

        if self.image != prev_image:
            try: # Delete the old image
                prev_image.delete(save=False)
            except:
                pass

        super().save(*args, **kwargs)

        if self.image != prev_image:
            try: # Generate the id of the image
                self.image_id = get_image_id(self.image.url)
            except ValueError: # If the image field has been cleared, clear the image_id field as well
                self.image_id = None
            super().save(update_fields=['image_id'])

    # def save(self, *args, **kwargs): # Only for updating the image_url field
    #     try:
    #         prev_instance = Event.objects.get(pk=self.pk)
    #         self.image_id = get_image_id(prev_instance.image.url)
    #     except:
    #         pass
    #     finally:
    #         super().save(*args, **kwargs)


    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    family = models.ForeignKey(to="Family", on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    image_id = models.CharField(blank=True, null=True, verbose_name="Profile image id (do not edit)")
    image = models.ImageField(blank=True, null=True, upload_to="profile_images", storage=gd_storage)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        try: # Check if the instance is being updated
            prev_image = Member.objects.get(pk=self.pk).image
        except Member.DoesNotExist: # If the instance is being created, set the previous image to None
            prev_image = None

        super().save(*args, **kwargs)

        if self.image != prev_image:
            try: # Generate the id of the image
                self.image_id = get_image_id(self.image.url)
            except ValueError: # If the image field has been cleared, clear the image_id field as well
                self.image_id = None
            super().save(update_fields=['image_id'])

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
