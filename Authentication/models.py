from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# ✅ Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # ✅ Securely hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with all permissions."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# ✅ Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    company_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    extra_field1 = models.CharField(max_length=255, blank=True, null=True)
    extra_field2 = models.CharField(max_length=255, blank=True, null=True)
    extra_field3 = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)  # ✅ Required for authentication
    is_staff = models.BooleanField(default=False)  # ✅ Required for admin access

    objects = UserManager()  # ✅ Attach custom manager

    USERNAME_FIELD = 'email'  # ✅ Define email as the login field
    REQUIRED_FIELDS = ['company_name', 'owner_name']  # Other required fields

    def __str__(self):
        return self.email
