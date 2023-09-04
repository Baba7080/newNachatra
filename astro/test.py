from django.test import TestCase
from django.shortcuts import render
from .models import *
import razorpay
from some.forms import *
from .forms import *
from django.conf import settings
import html
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your tests here.
def detail_pooja(request, pooja_id):
    instance = Pooja.objects.filter(id=pooja_id)
    # print(instance

    # Original data-settings attribute value

    return render(request, 'detail_pooja.html', {'detailpooja': instance})
def save_puja(request,pooja_id):
    if request.method == 'POST':
        form = PujaBook(request.POST)
        if form.is_valid():
            poojabooking = form.save(commit=False)
            poojabooking.userName  = form.cleaned_data['userName']
            poojabooking.mail  = form.cleaned_data['mail']
            poojabooking.phoneNo = form.cleaned_data['phoneNo']
            poojabooking.selectedDate = form.cleaned_data['selectedDate']
            poojabooking.selectedTime = form.cleaned_data['selectedTime']
            poojabooking.puja_id = pooja_id
            # poojabooking.userName = name
            # poojabooking.mail = mailId
            # poojabooking.phoneNo = no
            # poojabooking.selectedDate = dateofpooja
            # poojabooking.selectedTime = timeofpooja
            # print(poojabooking)
            booking = poojabooking.save()

            form = PujaBook()
            poojadetail = Pooja.objects.filter(id=pooja_id).values()
            poojaAmount=poojadetail[0]['price']
            # for i,k in poojadetail:
            #     # poojaAmount = i.price
            #     print(i+"=>"+k+"\n")
            payment = payment_view(pooja_id,poojaAmount)
            context ={
                'order': payment,
                'detail':poojadetail
                }
            # # rr= booking.save()
            # Redirect or render a success page
            return render(request, 'pay.html', {
                'order': payment,
                'detail':poojadetail
                })

    else:
        form = PujaBook()
    return render(request, 'payment.html', {'form': form})

def payment_view(id,amount):
    client = razorpay.Client(auth= (settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET))
    # amount = 10000  # Amount in paise
    order_currency = 'INR'

    data = {
        "amount": amount,
        "currency": order_currency,
        "payment_capture": 1,  # Unique order receipt
    }
    print(data)
    order = client.order.create(data)
    print(order)
    return order
    # return render('pay.html', {'order': order})
@login_required
def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            form = ContactForm()
            messages.success(request, 'Form submitted successfully!')
            # return redirect('success')
            return render(request,'contact.html',{'form':form})
            # Process the form data
    else:
        initial_data = {
            'name': request.user.username,    # Assuming 'name' is a field in your User model
            # 'number': request.user.number,  # Assuming 'number' is a field in your User model
            'email': request.user.email,    # Assuming 'email' is a field in your User model
        }
        # form = MyForm(initial=initial_data)
        form = ContactForm(initial=initial_data)
    return render(request,'contact.html',{'form': form})