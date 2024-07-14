from django.db import models
from django.contrib.auth.models import User
from gdstorage.storage import GoogleDriveStorage

gd_storage = GoogleDriveStorage()

def _get_image_id(url):
    """
    Strip the image id from the gdrive url of the image
    """
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

def _get_upload_path(instance, filename):
    """
    Generate the upload path for the image. This method is used so each subclass of CachedImageModel has its own images folder in google drive
    """
    return f"{instance.__class__.__name__.lower()}_images/{filename}"


class CachedImageModel(models.Model):
    """
    Abstract base class for models that have an image field
    """    
    image_id = models.CharField(blank=True, null=True, verbose_name="Image id (do not edit)")
    image = models.ImageField(blank=True, null=True, upload_to=_get_upload_path, storage=gd_storage)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        """
        Overridden save method. This handles the saving of the image to google drive and the generation of the image_id field.
        """
        # Check if we're updating or creating the an image
        try:
            prev_image = self.__class__.objects.get(pk=self.pk).image
        except self.__class__.DoesNotExist:
            prev_image = None
        
        # Call the parent save method. This also saves the image to google drive
        super().save(*args, **kwargs)

        # If the image has changed, cache the id of the new image
        if self.image != prev_image:
            try:
                self.image_id = _get_image_id(self.image.url)
            except ValueError:
                self.image_id = None
            super().save(update_fields=['image_id'])


class Event(CachedImageModel):
    """
    Event model
    """
    title = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    participants = models.ManyToManyField(to="Member", related_name="events", blank=True)
    venue = models.TextField()
    description = models.TextField(blank=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Member(CachedImageModel):
    """
    Member model
    """
    name = models.CharField(max_length=30, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    family = models.ForeignKey(to="Family", on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
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
