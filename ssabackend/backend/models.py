from django.db import models

# Create your models here.
class Event(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    participants = models.ManyToManyField(to="Member", related_name="events")
    venue = models.TextField()
    description = models.TextField()

class Member(models.Model):
    dob = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    family = models.ForeignKey(to="Family", on_delete=models.SET_NULL, null=True)
    profile_image = models.ImageField()

class Family(models.Model):
    fam_name = models.CharField()
    points = models.IntegerField()
    # score_log = models.ForeignKey(to="ScoreLog")

# class ScoreLog(models.Model):
#     date_uploaded = models.DateTimeField()
#     result = models.TextField()
#     score = models.IntegerField()
