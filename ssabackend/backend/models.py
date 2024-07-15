from django.db import models
from django.contrib.auth.models import User
from gdstorage.storage import GoogleDriveStorage


__all__ = ['Event', 'Member', 'Family', 'PhotoSubmission']

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
    telegram_username = models.CharField(max_length=30, blank=True, null=True, unique=True)
    telegram_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    family = models.ForeignKey(to="Family", on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Family(models.Model):
    """
    Family model
    """
    fam_name = models.CharField(max_length=30)
    points = models.FloatField(default=0)
    # score_log = models.ForeignKey(to="ScoreLog")

    def __str__(self):
        return self.fam_name
    

class PhotoSubmission(CachedImageModel):
    """
    Model for photo submissions
    """
    date_uploaded = models.DateTimeField(auto_now_add=True)
    family = models.ForeignKey(to="Family", on_delete=models.CASCADE, null=True, blank=True, related_name="photo_submissions")
    score = models.FloatField(default=0)
    member = models.ForeignKey(to="Member", on_delete=models.DO_NOTHING, null=True, blank=True, related_name="photo_submissions")
    description = models.TextField(blank=True)
    number_of_people = models.IntegerField(default=0)

    def _calculate_score(self) -> int:
        """
        Calculate the score of the photo submission
        """
        score = 0
        if self.description.lower() == "on-campus":
            score += 10
        elif self.description.lower() == "off-campus":
            score += 20
        
        if self.number_of_people > 3:
            score += self.number_of_people * 5 * 1.5
        else:
            score += self.number_of_people * 5
        self.score = score


    def save(self, *args, **kwargs):
        """
        Overridden save method. This handles the calculation of the score and populating of family field.
        """
        # Calculate the score
        self._calculate_score()
        
        # Set the family field
        self.family = self.member.family

        # Call the parent save method
        super().save(*args, **kwargs)
