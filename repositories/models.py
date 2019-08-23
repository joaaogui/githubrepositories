from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Repository(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    tag = models.ManyToManyField(Tag)