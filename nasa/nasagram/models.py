from django.db import models

# Create your models here.
class NasaComment(models.Model):
    date = models.DateField()
    comment = models.TextField()
    rating = models.IntegerField()
    favorite = models.BooleanField()
    image_url = models.URLField()

