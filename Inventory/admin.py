from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(Stock)
admin.site.register(Sale)
admin.site.register(SaleItem)