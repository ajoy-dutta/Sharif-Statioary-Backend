from rest_framework import generics
from .models import*
from .serializers import*

class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PaymentTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

class PaymentTypeDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

class GodownListCreateAPIView(generics.ListCreateAPIView):
    queryset = Godown.objects.all()
    serializer_class = GodownSerializer

class GodownDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Godown.objects.all()
    serializer_class = GodownSerializer