from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=20,default='')
    Second_Name = models.CharField(max_length=20,default='')
    bio =models.TextField(blank=True)
    code = models.CharField(max_length=8,blank=True)
    # recommended_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name='ref_by')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=200,default='city')
    Phone_Number = models.CharField(max_length=10,null=True)
    Role = models.CharField(max_length=10,null=True)
    # Category = models.CharField(max_length=100, choices=Catogories , default='STUDENT')
    image = models.ImageField(default='deafault.jpeg', upload_to='profile_pics')
    # is_pro = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}-{self.code}"

class Pooja(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=25,blank=False)
    description =models.TextField(blank=False)
    benifit = models.CharField(max_length=1000,blank=False)
    price = models.IntegerField(blank=True)
    image = models.ImageField(default='deafault.jpeg', upload_to='poojatype')
    # is_pro = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Name}"

from django import forms

class PujaForm(models.Model):
    userName = models.CharField(max_length=100)
    mail = models.EmailField()
    phoneNo = models.CharField(max_length=10)
    selectedDate = models.DateField()
    selectedTime = models.TimeField()
    puja_id = models.IntegerField()

    def __str__(self):
        return self.userName 

class Horoscope(models.Model):
    Name = models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    image = models.ImageField(default='deafault.jpeg', upload_to='poojatype')
    date =models.DateField()
    def __str__(self):
        return self.Name
    
class Services(models.Model):
    Name = models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    image = models.ImageField(default='deafault.jpeg', upload_to='client')
    date = models.DateField(default=timezone.now)
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return self.Name
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    number = models.IntegerField(blank=True)
    def __str__(self):
        return self.name