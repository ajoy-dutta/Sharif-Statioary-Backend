from django.db import models
from datetime import date

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_representative_name = models.CharField(max_length=255,null=True,blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    previous_due = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # New field for outstanding balance

    def __str__(self):
        return self.company_name

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=50, unique=True)
    product_description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.product_code} - {self.company.company_name}"

class PaymentType(models.Model):
    payment_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.payment_type

class Godown(models.Model):
    shop_name = models.CharField(max_length=255)
    godown_name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return f"{self.godown_name} ({self.shop_name})"


class Customer(models.Model):
    customer_id = models.CharField(max_length=20, editable=False)
    customer_name = models.CharField(max_length=255, default="Retail Customer")
    customer_address = models.TextField(blank=True, null=True)
    customer_phone_no = models.CharField(max_length=20, blank=True, null=True)
    customer_shop = models.CharField(max_length=255, blank=True, null=True)
    shop_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # New field for outstanding balance

    def save(self, *args, **kwargs):
        if not self.customer_id:
            if self.customer_name == "Retail Customer":
                self.customer_id = "123"
            else:
                # Generate new customer ID
                today_date = date.today().strftime('%d%m%Y')
                last_customer = Customer.objects.filter(customer_id__startswith=today_date).order_by('-customer_id').first()
                last_number = int(last_customer.customer_id.split('_')[-1]) + 1 if last_customer else 1
                self.customer_id = f"{today_date}_{last_number}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_id} - {self.customer_name}"
