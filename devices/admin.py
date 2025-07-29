# devices/admin.py

from django.contrib import admin
from .models import Device, ScheduledCommand, DayOfWeek
from django.utils.translation import gettext_lazy as _

# admin.site.site_header = "Controle do Sistema IoT" # Mesma mensagem do site_header do Jazzmin
# admin.site.site_title = "Controle IoT" # Mesma mensagem do site_title do Jazzmin
admin.site.index_title = "Painel" # Mensagem que aparece antes dos apps


class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'device_id',
        'name',
        'device_type',
        'location',
        'is_online',
        'last_seen',
        'last_command',
        'last_command_at'
    )
    list_filter = ('is_online', 'device_type', 'location')
    search_fields = ('name', 'device_id', 'location')
    readonly_fields = ('last_seen', 'created_at')
    fields = (
        'device_id',
        'name',
        'device_type',
        'location',
        'is_online',
        'data',
        'pending_command',
        'last_command_at',
        'last_command',
        'created_at',
    )


# Registre o modelo Device com suas configurações de admin
admin.site.register(Device, DeviceAdmin)


@admin.register(DayOfWeek)
class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ('name', 'numeric_value')
    ordering = ('numeric_value',)



@admin.register(ScheduledCommand)
class ScheduledCommandAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'schedule_type',
        'time_of_day',
        'run_once_at',
        'is_active',
        'last_triggered_at'
    )
    list_filter = (
        'schedule_type',
        'is_active',
        'day_of_week'
    )

    filter_horizontal = ('devices', 'day_of_week')

    search_fields = ('name', 'command_json')
    fieldsets = (
        (None, { 
            'fields': ('name', 'is_active', 'devices', 'command_json')
        }),
        (_('Detalhes do Agendamento'), { 
            'fields': ('schedule_type', 'day_of_week', 'time_of_day', 'run_once_at'),
            'description': _('Configure o tipo e os detalhes do agendamento. Preencha apenas os campos relevantes para o tipo selecionado.') # Já está traduzido
        }),
        (_('Informações de Status'), { 
            'fields': ('last_triggered_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('last_triggered_at',)
