import os

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from welsh.ludlow.models import Course, Profile


@receiver(post_save, sender=User)
def init_new_user(sender, instance, signal, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Course)
def create_course_folder_on_save(sender, instance, signal, created, **kwargs):
    if created:
        if not os.path.exists(instance.local_path):
            os.makedirs(instance.local_path)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
