from django.contrib import admin

# Register your models here.

from .models import Repository, OAuth2Token, Tag

admin.site.register(Repository)
admin.site.register(Tag)
admin.site.register(OAuth2Token)