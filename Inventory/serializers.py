from rest_framework import serializers
from .models import Item, PurchaseReceive, PaymentInformation  # ✅ Ensure all models are imported

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'  # ✅ Include all fields
class PurchaseReceiveSerializer(serializers.ModelSerializer):
    name_of_product = serializers.CharField()  # 🔹 Change from ForeignKey to CharField

    class Meta:
        model = PurchaseReceive
        fields = '__all__'  # ✅ Ensure all fields are included

# ✅ Payment Information Serializer
class PaymentInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInformation
        fields = '__all__'  # Include all fields