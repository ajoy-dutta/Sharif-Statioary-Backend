from rest_framework import generics  # Import generic views
from .models import Item, PurchaseReceive, PaymentInformation  # ✅ Ensure all models are imported
from .serializers import ItemSerializer, PurchaseReceiveSerializer, PaymentInformationSerializer  # ✅ Import all serializers

# ✅ API to show all items and add a new item
class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()  # Get all items from database
    serializer_class = ItemSerializer  # Convert items to JSON

# ✅ API to get, update, or delete one item
class ItemRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'id'  # Use 'id' to find item
# ✅ API for Retrieving, Updating, Deleting a Single Item
class ItemRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'id'

# ✅ API for Listing & Creating Purchase Receive
class PurchaseReceiveListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseReceive.objects.all()
    serializer_class = PurchaseReceiveSerializer

# ✅ API for Retrieving, Updating, Deleting a Single Purchase Receive
class PurchaseReceiveRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseReceive.objects.all()
    serializer_class = PurchaseReceiveSerializer
    lookup_field = 'id'

# ✅ API for Listing & Creating Payment Information
class PaymentInformationListCreateView(generics.ListCreateAPIView):
    queryset = PaymentInformation.objects.all()
    serializer_class = PaymentInformationSerializer

# ✅ API for Retrieving, Updating, Deleting a Single Payment Information
class PaymentInformationRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentInformation.objects.all()
    serializer_class = PaymentInformationSerializer
    lookup_field = 'id'
