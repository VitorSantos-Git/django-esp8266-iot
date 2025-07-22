# devices/admin.py
from django.contrib import admin
from .models import Device

# Classe para personalizar a exibição do modelo Device no admin
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'device_id', 'device_type', 'location', 
        'is_online', 'last_seen', 'last_command', 'last_command_at'
    )
    list_filter = ('is_online', 'device_type', 'location')
    search_fields = ('name', 'device_id', 'location')
    readonly_fields = ('last_seen', 'created_at') # Campos que não podem ser editados manualmente

# Registra o modelo Device com a personalização DeviceAdmin
admin.site.register(Device, DeviceAdmin)