from django.urls import path
from .views import*


urlpatterns = [

    path('purchases/', PurchaseCreateView.as_view(), name='payment-list-create'),
    path("api/purchases/<int:pk>/", PurchaseRetrieveUpdateDestroyView.as_view(), name="purchase-detail"),
]
