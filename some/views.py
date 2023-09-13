from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, SellerRegistrationForm
from astro .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils import timezone
import datetime
@csrf_exempt
def home(request):
    # astro_users = Profile.objects.filter(Role='Astro')
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    # today = timezone.now().date()
    Horoscopes = Horoscope.objects.filter(date=today)
    # Horoscopes = Horoscope.objects.all()
    service = Pooja.objects.all()
    # print(Horoscopes)
    # for i in Horoscopes:
    #     print(i.image.url )
    context = {'Horoscope': Horoscopes ,"profile":"2",'services':service}
    return render(request, 'home.html',context)
def logout(request):
    return redirect('login')
def about(request):
    client = Services.objects.filter(is_approved=True)
    # print(client)
    for i in client:
        print(i.description)
        print("\n")
    return render(request,'aboutus.html',{'client':client})
# views.py
@csrf_exempt
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # if profile_id is not None:
            #     recommended_by_profile = Profile.objects.get(id=profile_id)
            #     print('profile',recommended_by_profile)
            #     instance = form.save()
            #     register_user = User.objects.get(id=instance.id)
            #     register_profile = Profile.objects.get(user =register_user)
            #     register_profile.recommended_by = recommended_by_profile.user
            #     register_profile.save()
            # else:
            form.save()
            user = form.save(commit=False)
            user.is_active = True
            print("1 active = flse")
            user.save()
            
         
            return render(request , 'login.html')

    else:
        form = UserRegistrationForm()
    return render(request, 'user_registration.html', {'form': form})
    # if request.method == 'POST':
    #     form = UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         # Process form data and create user account
    #         return redirect('login')  # Redirect to login page
    # else:
    #     form = UserRegistrationForm()
    # return render(request, 'user_registration.html', {'form': form})
@csrf_exempt
def seller_registration(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save(commit=False)
            user.is_active = True
            print("1 active = flse")
            user.save()
            
            return redirect('login')  # Redirect to login page
    else:
        form = SellerRegistrationForm()
    return render(request, 'user_registration.html', {'form': form})

def Ourservices(req):
    service = Pooja.objects.all()
    # print(Horoscopes)
    # for i in Horoscopes:
    #     print(i.image.url )
    today = datetime.datetime.now().strftime("%Y-%m-%d")


    # # Filter data based on today's date
    # filtered_data = YourModel.objects.filter(your_date_field__date=today)
    Horoscopes = Horoscope.objects.filter(date=today)
    for i in Horoscopes:
        print(i)
    context = {'services':service,'Horoscope':Horoscopes}

    return render(req,'Services.html',context)
def gallery(req):
    images = Gallery.objects.all()
    print(images)
    for i in images:
        print(i.image)
    return render(req,'gallery.html',{'images':images})

def allpooja(req):
    poojas = Pooja.objects.all()
    return render(req,'allpooja.html',{'pooja':poojas})

def allhoros(req):
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    Horoscopes = Horoscope.objects.filter(date=today)
    # Horoscopes = Horoscope.objects.all()
    print(Horoscopes)
    return render(req,'horoscope.html',{'Horoscopess':Horoscopes})

def detailhoroscope(req,horosid):
    print(horosid)
    Horoscopes = Horoscope.objects.filter(id=horosid)
    return render(req,'detailhoroscope.html',{'Horoscope':Horoscopes})