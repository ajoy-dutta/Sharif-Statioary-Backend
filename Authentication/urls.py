from django.urls import path
from .views import*

urlpatterns = [
    path('persons/', ProductListCreateView.as_view(), name='persons'),  # API route

]