from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# model

from user_profile.models import Profile

# built-in imports 
import string
import random

# 3.PARTY Imports
from autoslug import AutoSlugField
from slugify import slugify


class Url(models.Model):
    base_url = models.URLField()
    shortened_slug = AutoSlugField(populate_from='set_slug', slugify=slugify, unique=True, editable=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    view_count = models.BigIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=('shortened_slug',))
        ]


    def set_slug(self):
        characters = string.ascii_letters + string.digits
        result = ''.join(random.choice(characters.lower()) for i in range(5))
        return result
    
    def get_url(self):
        return self.url
    
    def get_absolute_url(self):
        return reverse('shortener:redirecter_view', kwargs={'shortened_slug':self.shortened_slug})