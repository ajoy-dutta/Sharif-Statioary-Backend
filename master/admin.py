from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Godown)
admin.site.register(PaymentType)
admin.site.register(Customer)
