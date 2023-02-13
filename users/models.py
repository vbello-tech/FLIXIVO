from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
#from phonenumber_field.modelfields import PhoneNumberField
from django.shortcuts import reverse
from django.utils import timezone
from blog .models import *

# Create your models here.


class UserProfile(models.Model):
    person = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE,  blank=True, null=True)
    profile_pic = models.ImageField(blank=True, upload_to="Profile/")
    bio = models.TextField(blank=True)
    #phone_number = PhoneNumberField(blank=True, null=True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name="following", blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name="followers", blank=True)
    profile_id = models.IntegerField(blank=True, null=True)

    def follow(self):
        return reverse("user:follow", kwargs={
            'pk': self.pk,
        })

    def __str__(self):
        return f"{self.person}  profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_profile(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(person=instance, profile_id=instance.pk)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, created, *args, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        UserProfile.objects.create(person=instance, profile_id=instance.pk)
