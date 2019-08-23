from django.contrib import admin

# Register your models here.

from .models import Repository, Tag

admin.site.register(Repository)
admin.site.register(Tag)