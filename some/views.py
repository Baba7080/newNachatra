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
# import msg91_sms as msgsms
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
# @csrf_exempt
# def user_registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             # if profile_id is not None:
#             #     recommended_by_profile = Profile.objects.get(id=profile_id)
#             #     print('profile',recommended_by_profile)
#             #     instance = form.save()
#             #     register_user = User.objects.get(id=instance.id)
#             #     register_profile = Profile.objects.get(user =register_user)
#             #     register_profile.recommended_by = recommended_by_profile.user
#             #     register_profile.save()
#             # else:
#             form.save()
#             user = form.save(commit=False)
#             user.is_active = True
#             print("1 active = flse")
#             user.save()
            
         
#             return render(request , 'login.html')

#     else:
#         form = UserRegistrationForm()
#     return render(request, 'user_registration.html', {'form': form})
#     # if request.method == 'POST':
#     #     form = UserRegistrationForm(request.POST)
#     #     if form.is_valid():
#     #         # Process form data and create user account
#     #         return redirect('login')  # Redirect to login page
#     # else:
#     #     form = UserRegistrationForm()
#     # return render(request, 'user_registration.html', {'form': form})

def sendUsingtwilo(mobile,otp):
    account_sid = 'ACcc46a35823c5f59e6fc4b58963e51ffd'
    auth_token = '84b7472be0fc0b08081ac287598befae'
    
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                                from_='+14786548313',
                                body ='Nakshtravani validation code your four digit otp is '+otp,
                                to ='+91'+mobile
                            )
    
    print(message.sid)
    print(message)
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

            # print(rr)
            # print(token)
            # if profile_id is not None:
            #     recommended_by_profile = Profile.objects.get(id=profile_id)
            #     print('profile',recommended_by_profile)
            #     instance = form.save()
            #     register_user = User.objects.get(id=instance.id)
            #     register_profile = Profile.objects.get(user =register_user)
            #     register_profile.recommended_by = recommended_by_profile.user
            #     register_profile.save()
            # else:
            # create_profile = Profile.objects.create()
            # user_check = authenticate()
            
            new_user = authenticate(username=usernames,password=form.cleaned_data['password1'])
            aaa= login(request, new_user)
            print(aaa)

            print("1 active = flse")
            user.save()
            
            return redirect('home')
            # return render(request , 'home.html')

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
    verified_number =no
    # Initialize client outside of the if statements
    client = Client(account_sid, auth_token)
    print(client)
    if request.method == 'GET':
        print('in get')
        verification = client.verify.v2.services(verify_sid) \
            .verifications \
            .create(to=verified_number, channel="sms")
        return render(request, 'otp.html', {'username': useer})

    if request.method == 'POST':
        name = request.POST.get('otp')
        print(name)
        print(type(name))
        
        try:
            verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=no, code=name)
            print(verification_check.status)
            if verification_check.status == 'approved':
                print("valid otp")
                new_user = authenticate(username=pro.username, password=passw)
                if new_user:
                    login(request, new_user)
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
# def otpValidates(request,useer):
#     pro = User.objects.get(id=useer)
#     print(pro.username)
#     profileData = Profile.objects.filter(user=pro)

#     for i in profileData:
#         # print("hhhhhh")
#         passw = i.bio
#         valid = i.code
#         no = i.Phone_Number
#         print(i.code)
#     account_sid = "ACcc46a35823c5f59e6fc4b58963e51ffd"
#     auth_token = "84b7472be0fc0b08081ac287598befae"
#     verify_sid = "VAd7d8eca65193bbd4179f77df7b0fa608"
#     verified_number = "+91"+no

#     client = Client(account_sid, auth_token)

#     verification = client.verify.v2.services(verify_sid) \
#     .verifications \
#     .create(to=verified_number, channel="sms")
#     # print(pro.password1)
    
#     if request.method == 'POST':
#         # print(req)
#         print(useer)
#         pro = User.objects.get(id=useer)
#         print(pro.username)
#         # print(pro.password1)
#         profileData = Profile.objects.filter(user=pro)
#         # print(profileData.code)
#         name = request.POST.get('otp')
#         for i in profileData:
#             # print("hhhhhh")
#             passw = i.bio
#             valid = i.code
#             no = i.Phone_Number
#             print(i.code)
#         print(passw)
        
#         verification_check = client.verify.v2.services(verify_sid) \
#         .verification_checks \
#         .create(to=no, code=name)
#         print(verification_check.status)
#         if(verification_check.status == 'approved'):
#             print("valid otp")
#             new_user = authenticate(username=pro,password=passw)
#             aaa= login(request, new_user)
#             return redirect('home')
#         else:
#             return redirect('user_registration')


#         print(name)
    

#     # otps/<str:useer> [name='otps']
#     return render(request,'otp.html',{'username':useer})

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
    print(Horoscopes)
    return render(req,'horoscope.html',{'Horoscopess':Horoscopes})

def detailhoroscope(req,horosid):
    print(horosid)
    Horoscopes = Horoscope.objects.filter(id=horosid)
    return render(req,'detailhoroscope.html',{'Horoscope':Horoscopes})