from django.db import models

class Repository(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    tag = models.CharField(max_length=100)
    search_date = models.DateTimeField('date searched')