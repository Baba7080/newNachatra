from astro.models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# @receiver(post_save, sender=User)
# def post_save_create_profile(sender, instance, created, *args, **kwargs):
#     if created:
#         print(instance)
#         Profile.objects.create(
#             user=instance,
#             First_Name=instance.first_name
            
#             )