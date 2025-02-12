# Authentication/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['company_name', 'owner_name', 'phone1', 'phone2', 'email', 'password', 'extra_field1', 'extra_field2', 'extra_field3']
