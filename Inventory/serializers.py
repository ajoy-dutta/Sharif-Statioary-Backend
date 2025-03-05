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
