"""some URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib import admin
from django.urls import path
from .forms import LoginForm
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from astro.test import *
from astro.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home,name="home"),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    path('register/user/', user_registration, name='user_registration'),
    path('register/seller/', seller_registration, name='seller_registration'),
    path('pooja/<int:pooja_id>/', detail_pooja, name='detailpooja'),
    path('bookpooja/<int:pooja_id>/',save_puja,name='bookpooja'),
    path('aboutUs/',about,name='aboutUs'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logoutt'),name='logout'),
    path('logoutt/',logout,name='logoutt'),
    path('services/',Ourservices,name='services'),
    path('contactUs/',contactus,name='contactUs'),
    path('accounts/profile/',home,name='home'),
    path('gallery',gallery,name='gallery'),
    path('allpooja/',allpooja,name='allpooja'),
    path('horoscopes/',allhoros,name="horoscopes"),
    path('detailhoroscope/<int:horosid>/',detailhoroscope,name='detailhoroscope'),
    path('otps/<int:useer>',otpValidates,name='otps'),
    path('loginphone',loginphone,name='loginphone')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)