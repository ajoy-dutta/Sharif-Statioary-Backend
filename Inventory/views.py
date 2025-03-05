
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import*
from .serializers import*

class PurchaseCreateView(generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can create

    def perform_create(self, serializer):
        serializer.save(entry_by=self.request.user.username)
        
class PurchaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific purchase.
    """
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

class StockListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Stock.objects.all() 
    serializer_class = StockSerializer  


class SaleListCreateView(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def perform_create(self, serializer):
        sale = serializer.save()
        return sale

class SaleDetailView(generics.RetrieveAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer