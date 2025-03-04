from django.urls import path
from .views import*

urlpatterns = [
    path('companies/', CompanyListCreateAPIView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDestroyUpdateAPIView.as_view(), name='company-detail'),

    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDestroyUpdateAPIView.as_view(), name='product-detail'),

    path('payment-types/', PaymentTypeListCreateAPIView.as_view(), name='paymenttype-list-create'),
    path('payment-types/<int:pk>/', PaymentTypeDestroyUpdateAPIView.as_view(), name='paymenttype-detail'),

    path('godowns/', GodownListCreateAPIView.as_view(), name='godown-list-create'),
    path('godowns/<int:pk>/', GodownDestroyUpdateAPIView.as_view(), name='godown-detail'),
]