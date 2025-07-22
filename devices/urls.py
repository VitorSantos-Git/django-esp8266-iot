# devices/urls.py
from django.urls import path
from .views import DeviceAPIView

"""
urlpatterns = [
    path('device/', DeviceAPIView.as_view(), name='device_api'),
]
"""

urlpatterns = [
    # Endpoint para POST (enviar dados do ESP para o Django)
    path('device/', DeviceAPIView.as_view(), name='device_create_update'),
    
    # Endpoint para GET (ESP consultar comandos do Django)
    # <str:device_id> captura o ID do dispositivo na URL
    path('device/<str:device_id>/', DeviceAPIView.as_view(), name='device_command_query'),
]