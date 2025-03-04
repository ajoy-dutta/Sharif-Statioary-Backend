
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('api/auth/', include('Authentication.urls')),  
    # Include the Authentication app URLs
    path('', views.home),  # Root path should now point to the home view
     path('api/', include('Inventory.urls')),  
=======
    path('api/', include('Authentication.urls')),
    path('api/',include('master.urls')),
    path('api/',include('Inventory.urls')),
    path('api-auth/', include('rest_framework.urls')),

>>>>>>> c5ed091b57f9c2e25e30d41fed4a12dcfa6cd6aa
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
