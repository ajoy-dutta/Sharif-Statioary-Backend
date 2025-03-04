from django.urls import path
from .views import*

urlpatterns = [
    path("purchases/", PurchaseCreateView.as_view(), name="purchase-create"),

]