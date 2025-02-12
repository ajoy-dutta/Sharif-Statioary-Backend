from django.db import models

class Person(models.Model):
    company_name = models.CharField(max_length=255, null=True, blank=True)  # Company name field
    owner_name = models.CharField(max_length=255, null=True, blank=True)  # Owner name field
    phone_number_1 = models.CharField(max_length=15, unique=True, null=True, blank=True)  # Phone number 1 field
    phone_number_2 = models.CharField(max_length=15, unique=True, null=True, blank=True)  # Phone number 2 field
    address = models.TextField(null=True, blank=True)  # Address field
    email = models.EmailField(unique=True, null=True, blank=True)  # Email field
    password = models.CharField(max_length=255)  # Password field

    def __str__(self):
        return self.company_name  # You can change this to return any other field as well
