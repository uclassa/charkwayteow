from django.db import models
from django.contrib.auth.models import User
from gdstorage.storage import GoogleDriveStorage

__all__ = ['Event', 'Member', 'Family', 'PhotoSubmission']

gd_storage = GoogleDriveStorage()

#########################
##  Utility functions  ##
#########################

def get_image_id(url):
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


def get_upload_path(instance, filename):
    """
    Generate the upload path for the image.
    This method gives each subclass of CachedImageModel its own image folder in google drive
    """
    return f"{instance.__class__.__name__.lower()}_images/{filename}"

###############################
##  Model class definitions  ##
###############################

class CachedImageModel(models.Model):
    """
    Abstract base class for models that have an image field
    """
    image_id = models.CharField(blank=True, null=True, verbose_name="Image id (do not edit)")
    image = models.ImageField(blank=True, null=True, upload_to=get_upload_path, storage=gd_storage)

    class Meta:
        abstract = True

    @property
    def image_url(self):
        if self.image_id is None:
            return None
        return f"https://lh3.googleusercontent.com/u/0/d/{self.image_id}"

    def save(self, *args, **kwargs):
        """
        Overridden save method.
        Handles the saving of the image to google drive and the generation of the image_id field.
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
                self.image_id = get_image_id(self.image.url)
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
    visible = models.BooleanField(default=True)

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
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Family(models.Model):
    """
    Family model
    """
    fam_name = models.CharField(max_length=30)
    points_adjustment = models.FloatField(default=0)

    @property
    def points(self):
        """
        Calculate the total points of the family
        """
        result = self.photo_submissions.aggregate(models.Sum('score'))['score__sum']
        return (result if result else 0) + self.points_adjustment

    def __str__(self):
        return self.fam_name


class PhotoSubmission(CachedImageModel):
    """
    Model for photo submissions
    """
    date_uploaded = models.DateTimeField(auto_now_add=True)
    family = models.ForeignKey(to="Family", on_delete=models.CASCADE, null=True, blank=True, related_name="photo_submissions")
    score = models.FloatField(blank=True, verbose_name="Score (leave blank to auto-calculate)")
    member = models.ForeignKey(to="Member", on_delete=models.SET_NULL, null=True, related_name="photo_submissions")
    description = models.TextField(blank=True, choices={
        "random": "On-campus random encounter",
        "fun": "On-campus fun event",
        "single": "Off-campus single fam event",
        "crossover": "Off-campus crossover fam event",
        "ssa": "SSA-wide event"
    })
    number_of_people = models.IntegerField(default=0)

    def calculate_score(self):
        """
        Calculate the score of the photo submission.
        @property is not used here to avoid unnecessary computation when calculating total points of each fam
        """
        if not self.score is None: # do not recalculate the score if field is already filled
            return
        self.score = 0
        match self.description:
            case "ssa":
                self.score = self.number_of_people * 7
            case "random":
                self.score = (self.number_of_people-1) * 2
            case "fun":
                self.score = (self.number_of_people-1) * 5
            case "single":
                self.score = (self.number_of_people-1) * 5 + 10
            case "crossover":
                self.score = (self.number_of_people-1) * 5 + 30
                        

    def save(self, *args, **kwargs):
        """
        Overridden save method.
        Handles the calculation of the score and populating of family field.
        """
        # Calculate the score
        self.calculate_score()

        # Set the family field
        self.family = self.member.family

        # Call the parent save method
        super().save(*args, **kwargs)


class GroupChat(models.Model):
    """
    Model for group chats
    """
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title