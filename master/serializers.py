from rest_framework import serializers
from .models import*

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)  # Keeps full company details in response
    company_id = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), source='company', write_only=True)  # Allows posting with company_id

    class Meta:
        model = Product
        fields = ['id', 'company', 'company_id', 'product_code', 'product_name','product_type','date']


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'

class GodownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Godown
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
