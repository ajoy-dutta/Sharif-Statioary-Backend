from django.urls import path
from .views import*


urlpatterns = [

    path('purchases/', PurchaseCreateView.as_view(), name='payment-list-create'),
    # path('payments/<int:id>/', PaymentInformationRetrieveUpdateDeleteView.as_view(), name='payment-detail'),
]
