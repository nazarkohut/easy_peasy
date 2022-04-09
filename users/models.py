from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='userprofile', null=True)
    bio = models.TextField(max_length=256)
    location = models.CharField(max_length=128)
    image = models.ImageField(upload_to='profile_images/', default=None)

    class Meta:
        db_table = "user_profile"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


# setting User email field to be unique
User._meta.get_field('email')._unique = True
