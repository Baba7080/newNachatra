from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login

from .models import *
# Create your views here.
def loginphone(request):
    if request.method == 'POST':
        number = request.POST.get('phoneno')
        print(number)
        profiledata = Profile.objects.filter(Phone_Number=number)
        print(profiledata)
        if(profiledata):
            for pro in profiledata:
                usernames = pro.user
                passw = pro.bio
            new_user = authenticate(username=usernames, password=passw)
            if new_user:
                login(request, new_user)
                return redirect('home')
            else:
                return redirect('user_registration')
        else:
            return redirect('user_registration')
    return render(request,'loginphone.html')