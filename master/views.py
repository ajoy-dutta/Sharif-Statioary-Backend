from rest_framework import generics
from .models import*
from .serializers import*
from rest_framework.permissions import IsAuthenticated,AllowAny

class CompanyListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
   
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PaymentTypeListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

class PaymentTypeDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

class GodownListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Godown.objects.all()
    serializer_class = GodownSerializer

class GodownDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Godown.objects.all()
    serializer_class = GodownSerializer