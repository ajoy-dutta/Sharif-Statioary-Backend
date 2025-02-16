from django.contrib import admin
from .models import User  # Import your custom User model

class UserAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'owner_name', 'email', 'phone1', 'phone2', 'is_active', 'is_staff']  # Added 'is_staff'
    search_fields = ['company_name', 'owner_name', 'email']
    list_filter = ['is_active', 'is_staff']  # Added 'is_staff' filter
    ordering = ['email']  # Order users by email in the admin list view

# Register the User model with the customized admin class
admin.site.register(User, UserAdmin)
