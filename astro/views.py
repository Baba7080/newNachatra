from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from some.forms import UserRegistrationForm, SellerRegistrationForm
from .models import *
# Create your views here.
def loginphone(request):
    next_url = request.GET.get('next', '')
    print(next_url)
    if request.method == 'POST':
        number = request.POST.get('phoneno')
        nexturl = request.POST.get('next')
        print(nexturl)
        print("post loginphone")
        print(number)
        profiledata = Profile.objects.filter(Phone_Number=number)
        print(profiledata)
        if(profiledata):
            for pro in profiledata:
                usernames = pro.user
                passw = pro.bio
            user = User.objects.filter(username=usernames)
            print(user)
            for users in user:
                ids = users.id
            if nexturl is not None:
                return redirect(f'/otps/{ids}/?next={nexturl}')
            return redirect('/otps/{}'.format(ids))
            
            new_user = authenticate(username=usernames, password=passw)
            if new_user:
                login(request, new_user)
                return redirect('home')
            else:
                return redirect('user_registration')
        else:
            passs = number+"Nakshtravani@"
            passs = str(passs)
            print(passs)
            user = User.objects.create(
                username=number
                # role='User',
                # password=passs,
            )
            v = user.set_password(passs)
            print(v)
            user.save()
            user = User.objects.get(username=number)
            # user.is_active = False
            user.passwo = passs

            createProfile = Profile.objects.create(user=user,Phone_Number=number,Role='User',bio=passs)
            user.save()
            # print(createProfile)
            # print(user.id)
            # print(user)
            # print("ghgjjhhgghgf")
            return redirect('/otps/{}'.format(user.id))
    if next_url is not None:
        return render(request,'loginphone.html',{"next":next_url})
    else:
        return render(request,'loginphone.html')