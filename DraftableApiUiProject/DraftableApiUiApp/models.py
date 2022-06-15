from operator import mod
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


def input_files_location(instance, filename):
    return "pdf_files/{file}".format(file=filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserFiles(models.Model):
    left_file = models.FileField(upload_to=input_files_location,
                                 verbose_name="Older version File(Left)")
    right_file = models.FileField(upload_to=input_files_location,
                                  verbose_name="Older version File(Right)")
