from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from django.contrib.auth.models import User

from autoslug import AutoSlugField
from slugify import slugify

# signalling
from django.db.models.signals import post_save
from django.dispatch import receiver

# rest_framework token
from rest_framework.authtoken.models import Token

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='get_username', unique=True, slugify=slugify)
    info = models.TextField(null=True,blank=True)
    premium = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='user-avatars/', default='user-avatars/github-logo.png', blank=True, null=True)
    api_view = models.BigIntegerField(default=0)
    api_create = models.BigIntegerField(default=0)
    
    def update_premium_1(self):
        self.premium = True
        self.api_view = 30000
        self.api_create = 1000

    def get_username(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('user_profile:profile_detail_view', kwargs={'profile_slug':self.slug})
    
    def __str__(self):
        return f'{self.user}'
    
