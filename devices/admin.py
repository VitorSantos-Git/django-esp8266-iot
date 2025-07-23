# devices/admin.py

from django.contrib import admin
from .models import Device, ScheduledCommand, DayOfWeek

# Classe para personalizar a exibição do modelo Device no admin
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'device_id', 'device_type', 'location', 
        'is_online', 'last_seen', 'last_command', 'last_command_at'
    )
    list_filter = ('is_online', 'device_type', 'location')
    search_fields = ('name', 'device_id', 'location')
    readonly_fields = ('last_seen', 'created_at') # Campos que não podem ser editados manualmente
    fields = (
        'device_id', 'name', 'device_type', 'location', 
        ('last_seen', 'is_online'),
        'data',
        'pending_command',
        ('last_command', 'last_command_at'),
        'created_at',
    )

# Registra o modelo Device com a personalização DeviceAdmin
admin.site.register(Device, DeviceAdmin)

@admin.register(DayOfWeek)
class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ('name', 'numeric_value')
    ordering = ('numeric_value',)

@admin.register(ScheduledCommand)
class ScheduledCommandAdmin(admin.ModelAdmin):
    list_display = ('name', 'schedule_type', 'time_of_day', 'run_once_at', 'is_active', 'last_triggered_at')
    list_filter = ('schedule_type', 'is_active', 'day_of_week')
    filter_horizontal = ('devices', 'day_of_week') # Melhora a interface para ManyToMany
    search_fields = ('name', 'command_json')
    fieldsets = (
        (None, {
            'fields': ('name', 'is_active', 'devices', 'command_json')
        }),
        ('Detalhes do Agendamento', {
            'fields': ('schedule_type', 'day_of_week', 'time_of_day', 'run_once_at'),
            'description': 'Configure o tipo e os detalhes do agendamento. Preencha apenas os campos relevantes para o tipo selecionado.'
        }),
        ('Informações de Status', {
            'fields': ('last_triggered_at',),
            'classes': ('collapse',), # Colapsa esta seção por padrão
        }),
    )
    readonly_fields = ('last_triggered_at',)