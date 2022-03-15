from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings 
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

@receiver(post_save, sender=User)
def create__doctor_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)