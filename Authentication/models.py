from django.db import models
from .models import*
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=40, default='General', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='image/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
            self.is_approved = True
        elif not self.role:  # If the role is not provided, assign the default 'Assistant Accountant'
            self.role = 'General'
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return self.username
