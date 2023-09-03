from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from time import time
import datetime
from datetime import time
from django.contrib.auth.models import User
from  .models import *
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from django.views.decorators.csrf import csrf_exempt


class ContactForm(forms.ModelForm):
    # Define user registration fields here (e.g., username, email, password)
    # Name = forms.CharField(label="Enter your Name")
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':"form-control"}))
    subject = forms.CharField(label="Enter the Topic ")
    message = forms.CharField(label="Enter Message if any")
    class Meta:
        model = Contact
        # fields = ['Name','subject','message','email']
        fields = "__all__"
        # label = {'email':'Email'}
        # widget = {'username':forms.TextInput(attrs={'class':'form-control'})}
    # def save(self,commit=True):
    #     instance = super().save(commit=False)
    #     instance.some_flag = True
    #     print(instance)
    #     if commit:
    #         instance.save()
    #         self.save_m2m()
    #     return instance