from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, SellerRegistrationForm
from astro .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils import timezone
import datetime
import random 
import http.client
from django.conf import settings
from django.contrib.auth import authenticate,login
from twilio.rest import Client
from django.urls import reverse
from twilio.base.exceptions import TwilioRestException
from user.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def my_view(request, random_url):
    # Do something with the random_url parameter
    return HttpResponse(f"You entered the random URL: {random_url}")
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
    return render(request, 'index.html',context)
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
            phone_no = request.POST.get('phone')
            name = request.POST.get('first_name')
            print(name)
            
            form.instance.username = name+f'{random.randrange(10000000)}'
            print(phone_no)
            usernames = form.instance.username
            password = form.cleaned_data['password1']
            print(form.instance.username)
            print(form.cleaned_data['password1'])
            # login(request, user)
            form.save()
            user = form.save()
            user.is_active = False
            check_profile = Profile.objects.filter(Phone_Number=phone_no).first()
            if(check_profile):
                print("yes")
                print(check_profile)
            otp = str(random.randint(1000 , 9999))
            print(otp)
            # userd = request.User
            createProfile = Profile.objects.create(user=user,Phone_Number=phone_no,Role='User',code=otp,bio=password)
            print(createProfile)
            # validate = otpValidate(request,usernames)
            # return redirect(f'/otp?{usernames}')
            print(user.id)
            context={'useer': usernames}
            # rr = sendUsingtwilo(phone_no,otp)
            # url = reverse('otp'
            # return render(request,'otp.html',context)
            return redirect('/otps/{}'.format(user.id))
            # if profile_id is not None:
            #     recommended_by_profile = Profile.objects.get(id=profile_id)
            #     print('profile',recommended_by_profile)
            #     instance = form.save()
            #     register_user = User.objects.get(id=instance.id)
            #     register_profile = Profile.objects.get(user =register_user)
            #     register_profile.recommended_by = recommended_by_profile.user
            #     register_profile.save()
            # else:
            # form.save()
            # user = form.save(commit=False)
            # user.is_active = True
            # print("1 active = flse")
            # user.save()

            
         
            # return render(request , 'login.html')

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

def otpValidates(request, useer):
    pro = User.objects.get(id=useer)
    next_url = request.GET.get('next', '')
    print(next_url)
    print("otp validate")

    print(pro.username)
    
    # You can simplify this query using get() if you expect only one profile per user
    profileData = Profile.objects.filter(user=pro)
    for i in profileData:
        # print("hhhhhh")
        passw = i.bio
        valid = i.code
        no = i.Phone_Number
        print(i.code)
    # passw = profileData.bio
    # valid = profileData.code
    # no = profileData.Phone_Number
    no = "+91"+no
    print(no)

    # print(profileData.code)
    account_sid = settings.ACCOUNT_SID
    auth_token =  settings.AUTH_TOKEN
    verify_sid = settings.VARIFY_SID
    SecurityToken = Security.objects.all()
    for token in SecurityToken:
        account_sid = token.ACCOUNT_SID
        auth_token = token.AUTH_TOKEN
        verify_sid = token.VARIFY_SID
    verified_number =no
    # Initialize client outside of the if statements
    client = Client(account_sid, auth_token)
    print(client)
    if request.method == 'GET':
        print('in get')
        verification = client.verify.v2.services(verify_sid) \
            .verifications \
            .create(to=verified_number, channel="sms")
        if next_url is not None:
            return render(request, 'otp.html', {'username': useer,'next':next_url})

        return render(request, 'otp.html', {'username': useer})

    if request.method == 'POST':
        name = request.POST.get('otp')
        next_url = request.POST.get('next')
        print(next_url)
        print(name)
        print(type(name))
        
        try:
            verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=no, code=name )
            print(verification_check.status)
            if verification_check.status == 'approved':
                print("valid otp")
                pro.is_active = True
                new_user = authenticate(username=pro.username, password=passw)

                if new_user:
                    login(request, new_user)
                    if next_url:
                        return redirect(next_url)
                    return redirect('home')
                else:
                    return redirect('user_registration')
            else:
                return redirect('user_registration')
        except TwilioRestException as e:
            # Handle Twilio API exception
            print(f"Twilio Error: {e}")
            return redirect('user_registration')

        
       

    return render(request, 'otp.html', {'username': useer})
@csrf_exempt
def seller_registration(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save(commit=False)
            user.is_active = False
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
    # print(Horoscopes)
    return render(req,'horoscope.html',{'Horoscopess':Horoscopes})

def detailhoroscope(req,horosid):
    print(horosid)
    Horoscopes = Horoscope.objects.filter(id=horosid)
    return render(req,'detailhoroscope.html',{'Horoscope':Horoscopes})
@login_required
def profiles(req):
    current_user = req.user
    print(current_user)
    current_profile = Profile.objects.filter(user=current_user)

    if current_profile.exists():
        for profile in current_profile:
            print(profile.bio)
        return render(req,'profile.html',{'profileData':current_profile})
@login_required  
def profileupdate(request,pid):
    if request.method == 'POST':
        print(pid)
        my_object = Profile.objects.get(id=pid)
        updateaddress = request.POST.get('address')
        updatefirstname = request.POST.get('firstname')
        updatelastname = request.POST.get('lastname')
        updatemail = request.POST.get('mail')
        updatePhoneNumber = request.POST.get('Phone_Number')
        updatecity = request.POST.get('city')
        updateaddress = request.POST.get('address')
        # assiging the new valuee to object 
        my_object.address = updateaddress
        my_object.First_Name = updatefirstname
        my_object.Second_Name = updatelastname
        my_object.mail = updatemail
        my_object.Phone_Number = updatePhoneNumber
        my_object.city = updatecity
        my_object.save()
        current_profile = Profile.objects.filter(id=pid)

        if current_profile.exists():
            return render(request,'profile.html',{'profileData':current_profile})


        print(request.POST.get('address'))
    profileData = Profile.objects.filter(id=pid)
    if profileData.exists():
        for profile in profileData:
            print(profile.bio)
        return render(request,'updateprofile.html',{'profiledatas':profileData})