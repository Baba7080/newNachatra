from django.db import models

# Create your models here.
class Security(models.Model):
    ACCOUNT_SID = models.CharField(blank=True,max_length=200)
    AUTH_TOKEN = models.CharField(blank=True,max_length=200)
    VARIFY_SID = models.CharField(blank=True,max_length=200)