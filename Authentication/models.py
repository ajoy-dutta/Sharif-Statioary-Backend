# Authentication/models.py
from django.db import models

class User(models.Model):
    company_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    extra_field1 = models.CharField(max_length=255, blank=True, null=True)
    extra_field2 = models.CharField(max_length=255, blank=True, null=True)
    extra_field3 = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.company_name
