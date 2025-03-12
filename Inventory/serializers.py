from rest_framework import serializers
from .models import*


class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        exclude = ['purchase']  # ✅ Exclude 'purchase' so it's auto-handled

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)  # ✅ Accept multiple items

    class Meta:
        model = Purchase
        fields = '__all__'  

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])  # ✅ Extract items list
        purchase = Purchase.objects.create(**validated_data)  # ✅ Create Purchase first
        
        for item_data in items_data:
            PurchaseItem.objects.create(purchase=purchase, **item_data)  # ✅ Link items to purchase
        
        return purchase



class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    
    class Meta:
        model = Stock
        fields = '__all__' 

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = '__all__'

    def create(self, validated_data):
        sale_items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)

        for item_data in sale_items_data:
            SaleItem.objects.create(sale=sale, **item_data)

        return sale