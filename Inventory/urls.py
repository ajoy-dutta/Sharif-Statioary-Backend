from django.urls import path
from .views import*


urlpatterns = [

    path('purchases/', PurchaseCreateView.as_view(), name='payment-list-create'),
    path("api/purchases/<int:pk>/", PurchaseRetrieveUpdateDestroyView.as_view(), name="purchase-detail"),
    path('stock/', StockListView.as_view(), name='stock-list'), 
    path('sales/', SaleListCreateView.as_view(), name='sale-list-create'),
    path('sales/<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
]
