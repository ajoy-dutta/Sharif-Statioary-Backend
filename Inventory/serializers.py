from rest_framework import serializers
from .models import*

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = '__all__'  # Include all fields

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)  # Allow multiple items in a single purchase

    class Meta:
        model = Purchase
        fields = '__all__'  # Include all fields including items

    def create(self, validated_data):
        """
        Override create to handle nested PurchaseItem data.
        """
        items_data = validated_data.pop('items')  # Extract items data
        purchase = Purchase.objects.create(**validated_data)  # Create the Purchase instance

        for item_data in items_data:
            PurchaseItem.objects.create(purchase=purchase, **item_data)  # Add items to purchase

        return purchase

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__' 

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    sale_items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = '__all__'

    def create(self, validated_data):
        sale_items_data = validated_data.pop('sale_items')
        sale = Sale.objects.create(**validated_data)

        for item_data in sale_items_data:
            SaleItem.objects.create(sale=sale, **item_data)

        return sale