from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_representative_name = models.CharField(max_length=255,null=True,blank=True)
 
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

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
