from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)  # Hide password in responses

    class Meta:
        model = User
        fields = ['company_name', 'owner_name', 'phone1', 'phone2', 'email', 'password', 'extra_field1', 'extra_field2', 'extra_field3']

    def create(self, validated_data):
        """Hash the password before saving the user."""
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        return super().create(validated_data)
