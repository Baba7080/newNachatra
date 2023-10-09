from django.test import TestCase
from django.shortcuts import render,redirect
from .models import *
import razorpay
from some.forms import *
from .forms import *
from django.conf import settings
import html
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import base64
import hashlib
import requests
from django.http import HttpResponse
import uuid
from user.models import *
from django.views.decorators.csrf import csrf_exempt
# Create your tests here.
def detail_pooja(request, pooja_id):
    instance = Pooja.objects.filter(id=pooja_id)
    # print(instance

    # Original data-settings attribute value

    return render(request, 'detail_pooja.html', {'detailpooja': instance})
@login_required(login_url='loginphone')
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
            # payment = patmentphonepay(pooja_id,poojaAmount)
            try:
                payment_secret = PaymentSecret.objects.first()  
                # payment_secret = True
                merchant = payment_secret.merchantid
                key = payment_secret.key
                if payment_secret:
                    print(merchant)
                    merchantTransactionId = str(uuid.uuid4())
                    userss = request.user
                    prof = Profile.objects.get(user=userss)
                    if(prof and prof.Phone_Number):
                        userId = prof.Phone_Number
                    else:
                        userId = userss
                    print(prof.Phone_Number)
                    baseurl = "https://www.nakshtravani.com/"
                    data = {
                        "merchantId": merchant,
                        "merchantTransactionId": merchantTransactionId,
                        "merchantUserId": str(userId),
                        "amount": poojaAmount * 100,
                        "redirectUrl": baseurl+"paymentsuccess/",
                        "redirectMode": "POST",
                        "callbackUrl": baseurl+"paymentsuccess/",
                        "mobileNumber": str(userss),
                        "paymentInstrument": {
                            "type": "PAY_PAGE"
                        }
                    }

                    # Convert the payload to JSON and encode as Base64
                    payload_main = base64.b64encode(json.dumps(data).encode()).decode()

                    payload = payload_main + "/pg/v1/pay" + key
                    checksum = hashlib.sha256(payload.encode()).hexdigest()
                    checksum = checksum + '###1'

                    header = {
                        "Content-Type": "application/json",
                        "X-VERIFY": str(checksum),
                        "accept": "application/json"
                    }

                    url = "https://api.phonepe.com/apis/hermes/pg/v1/pay"
                    payload_data = {
                        "request": payload_main
                    }
                    datas=json.dumps(payload_data)
                    print(datas)
                    # response = requests.post(url, data=json.dumps(payload_data), headers=header)
                    response = requests.request("POST", url, data=datas, headers=header)

                    print(response.text,response.status_code)
                    if response.status_code == 200:
                        response_data = response.json()
                        print("responce")
                        print(response)
                        url = response_data['data']['instrumentResponse']['redirectInfo']['url']
                        # Redirect to the obtained URL
                        print(url)
                        # name = models.CharField(max_length=100)
                        # amount = models.IntegerField()
                        # source = models.CharField(max_length=150)
                        # transaction_id = models.CharField(max_length=150)
                        # status = models.CharField(max_length=500)
                        initiate = PaymentInitiate.objects.create(name=userss,amount=poojaAmount,source=str(pooja_id),transaction_id=merchantTransactionId,status="Initiated")
                        # print("redirect")
                       
                        return redirect(url,permanent=True)

                        return HttpResponse(f"Redirecting to PhonePe: <a href='{url}'>{url}</a>")
                    else:
                        # Handle the error here
                        return HttpResponse(f"HTTP Error: {response.status_code}<br>{response.text}", status=500)
                else:
                    return HttpResponse("Payment secret not found", status=500)
            except Exception as e:
                # Handle other exceptions
                return HttpResponse(f"Error: {str(e)}", status=500)
            context ={
                'order': payment,
                'detail':poojadetail
                }
            # # rr= booking.save()
            # Redirect or render a success page
            return render(request, 'qr.html', {
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
    orderData = client.order.create(data)
    TotalAmount =  orderData['amount']
    dueAmount = orderData['amount_due']
    print(TotalAmount,dueAmount)
    createOrder = Order.objects.create(orderId=orderData['id'],amount=TotalAmount,amount_due=dueAmount,currency=orderData['currency'],status=orderData['status'],createdOntarget=orderData['created_at'])
    print(orderData)
    return orderData
    # return render('pay.html', {'order': order})
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
   
        # form = MyForm(initial=initial_data)
    form = ContactForm()
    return render(request,'contact.html',{'form': form})
@login_required
def save_payment(request,pooja_id):
    if request.method == 'POST':
        form = PaymentVarification(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            form = PaymentVarification()
            messages.success(request, 'Form submitted successfully!')
            # return redirect('success')
            return render(request,'qr.html',{'form':form})
    form = PaymentVarification()
    return render(request, 'qr.html', {'form': form})
@csrf_exempt
def paymentsuccess(request):
    print("success hoa ")
    print(request)
    if request.method == 'POST':
        print(request.GET)
        return HttpResponse(request)

    return HttpResponse(request)