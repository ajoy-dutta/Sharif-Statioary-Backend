from django.db import models
from datetime import date
from django.utils.timezone import now

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_representative_name = models.CharField(max_length=255,null=True,blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)  
    address = models.TextField(null=True, blank=True)
    previous_due = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.company_name

class Product(models.Model):
    PRODUCT_TYPES = [
        ('RIM-A4', 'RIM-A4'),
         ('DOZEN', 'DOZEN'),
        ('RIM-LEGAL', 'RIM-LEGAL'),
    ]
    product_name = models.CharField(max_length=255)  
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPES)
    product_code = models.CharField(max_length=50, unique=True, blank=True)
    date = models.DateField(default=now)  

    def save(self, *args, **kwargs):
        if not self.product_code:
            today = self.date.strftime('%d%m%Y')  
            
            product_count = Product.objects.filter(date=self.date).count() + 1

            self.product_code = f"{today}-{product_count}"  # Dynamic numbering
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.product_code} - {self.product_type} - {self.company.company_name}"

class PaymentType(models.Model):
    payment_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.payment_type

class Godown(models.Model):
    godown_name = models.CharField(max_length=255)  
    shop_name = models.CharField(max_length=255, null=True, blank=True)  
    address = models.TextField(null=True, blank=True)  

    def __str__(self):
        return f"{self.godown_name}"



class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_address = models.TextField(blank=True, null=True)
    customer_phone_no = models.CharField(max_length=20, blank=True, null=True)
    customer_shop = models.CharField(max_length=255, blank=True, null=True)
    shop_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # New field for outstanding balance


    def __str__(self):
        return f"{self.customer_name}"
