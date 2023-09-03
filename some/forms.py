from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from time import time
import datetime
from datetime import time
from django.contrib.auth.models import User
from astro .models import *
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from django.views.decorators.csrf import csrf_exempt


class UserRegistrationForm(UserCreationForm):
    # Define user registration fields here (e.g., username, email, password)
    Name = forms.CharField(label="Enter your Name" ,max_length=12)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':"form-control"}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':"form-control"}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':"form-control"}))
    Role = forms.CharField(initial="User",widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    date_of_join = forms.DateField(initial=datetime.date.today)
    # time_join = forms.DateTimeField(initial=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    time_of_join = forms.TimeField(initial=datetime.datetime.now)
    #  forms.DateTimeField(initial = datetime.datetime.now)
    # Category = forms.ChoiceField(choices = Catogories)
    class Meta:
        model = User
        fields = ['Name','username','Role','date_of_join','time_of_join','email','password1','password2']
        label = {'email':'Email'}
        widget = {'username':forms.TextInput(attrs={'class':'form-control'})}
    def save(self, commit=True):
        user = super().save(commit=False)
        user.passw = self.cleaned_data.get('password1')  # Copy the 'Name' field value to 'traffic'
        
        if commit:
            user.save()
        
        return user
class SellerRegistrationForm(UserCreationForm):
    Name = forms.CharField(label="Enter your Name" ,max_length=12)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':"form-control"}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':"form-control"}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':"form-control"}))
    Role = forms.CharField(initial="Astro",widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    date_of_join = forms.DateField(initial=datetime.date.today)
    # time_join = forms.DateTimeField(initial=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    time_of_join = forms.TimeField(initial=datetime.datetime.now)
    #  forms.DateTimeField(initial = datetime.datetime.now)
    # Category = forms.ChoiceField(choices = Catogories)
    class Meta:
        model = User
        fields = ['Name','username','Role','date_of_join','time_of_join','email','password1','password2']
        label = {'email':'Email'}
        widget = {'username':forms.TextInput(attrs={'class':'form-control'})}
    def save(self, commit=True):
        user = super().save(commit=False)
        user.passw = self.cleaned_data.get('password1')  # Copy the 'Name' field value to 'traffic'
        
        if commit:
            user.save()
        
        return user
@csrf_exempt
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs=
        {'autocomplete':'current-password', 'class':'form-control'}))



class PujaBook(forms.ModelForm):
    userName = forms.CharField(label='Full Name', max_length=100)
    mail = forms.EmailField(label='Email Address')
    phoneNo = forms.CharField(label='Contact Number')
    selectedDate = forms.DateField(label='Select a date', widget=forms.DateInput(attrs={'type': 'date'}))
    selectedTime = forms.TimeField(label='Select a time', widget=forms.TimeInput(attrs={'type': 'time'}))
    # puja_id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = PujaForm
        fields = ['userName','mail','phoneNo','selectedDate','selectedTime']
    # def save(self, commit=True):
    #     user = super().save(commit=False)