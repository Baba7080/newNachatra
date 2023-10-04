from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.register(Profile),
admin.site.register(Pooja)
admin.site.register(PujaForm)
admin.site.register(Horoscope)
admin.site.register(Services)
admin.site.register(Contact)
admin.site.register(Gallery)
admin.site.register(Order) 
admin.site.register(PaymentDetail) 
admin.site.register(PaymentInitiate)