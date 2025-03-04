from django.urls import path
from .views import (
    ItemListCreateView, ItemRetrieveUpdateDeleteView,
    PurchaseReceiveListCreateView, PurchaseReceiveRetrieveUpdateDeleteView,
    PaymentInformationListCreateView, PaymentInformationRetrieveUpdateDeleteView
)  # ✅ Ensure all views are imported

urlpatterns = [
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),  # ✅ List all & create
    path('items/<int:id>/', ItemRetrieveUpdateDeleteView.as_view(), name='item-detail'),  # ✅ Retrieve, update, delete
     # ✅ Purchase Receive API
    path('purchase-receive/', PurchaseReceiveListCreateView.as_view(), name='purchase-receive-list-create'),
    path('purchase-receive/<int:id>/', PurchaseReceiveRetrieveUpdateDeleteView.as_view(), name='purchase-receive-detail'),

    # ✅ Payment Information API
    path('payments/', PaymentInformationListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:id>/', PaymentInformationRetrieveUpdateDeleteView.as_view(), name='payment-detail'),
]
