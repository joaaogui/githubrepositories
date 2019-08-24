from django.db import models
from taggit.managers import TaggableManager

class Repository(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    tags = TaggableManager()