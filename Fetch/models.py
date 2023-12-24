from django.db import models

# Create your models here.

class Archive(models.Model):
    title = models.CharField(max_length=126, null=True, blank=True)
    author = models.CharField(max_length=126, null=True, blank=True)
    publish_date = models.CharField("Publish date (as string)", max_length=126, null=True, blank=True)
