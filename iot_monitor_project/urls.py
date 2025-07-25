# iot_monitor_project/urls.py
from django.contrib import admin
from django.urls import path, include 
from rest_framework.authtoken import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('devices.urls')), 
    path('api-token-auth/', views.obtain_auth_token), 
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    
]
