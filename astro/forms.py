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

from django.core.exceptions import ValidationError

def validate_10_digit_number(value):
    if len(str(value)) != 10:
        raise ValidationError('The number must be exactly 10 digits long.')

class ContactForm(forms.ModelForm):
    # Define user registration fields here (e.g., username, email, password)
    name = forms.CharField(label="Enter your Name",widget=forms.TextInput(attrs={'class':"form-control"}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':"form-control"}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}),label="Enter the Topic ")
    message = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}),label="Enter Message if any")
    number = forms.IntegerField(label="Enter Your Contact ",validators=[validate_10_digit_number], widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}))
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