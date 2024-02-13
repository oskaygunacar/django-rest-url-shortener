from django.contrib.auth.models import User

# signalling
from django.db.models.signals import post_save
from django.dispatch import receiver

# rest_framework token
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_token(sender, instance, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
