"""
URL configuration for sharif_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

# sharif_backend/urls.py
from django.contrib import admin
from django.urls import path, include

from django.contrib import admin
from django.urls import path, include
from sharif_backend import views  # Import views from the sharif_backend app

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('api/auth/', include('Authentication.urls')),  # Include the Authentication app URLs
    path('', views.home),  # Root path should now point to the home view
]


