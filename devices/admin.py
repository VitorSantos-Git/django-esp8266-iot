# devices/admin.py

from django.contrib import admin
from .models import Device, ScheduledCommand, DayOfWeek, DeviceDataHistory
from django.utils.translation import gettext_lazy as _
from import_export import resources # <-- Importe resources
from import_export.admin import ImportExportModelAdmin

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


class DeviceDataHistoryResource(resources.ModelResource):
    # Campos JSON são exportados como strings por padrão.
    class Meta:
        model = DeviceDataHistory
        # Defina os campos que você quer exportar
        fields = ('id', 'device__device_id', 'device__name', 'timestamp', 'data_payload')
        # Exclua campos exemplo
        # exclude = ('id',) 


@admin.register(DeviceDataHistory)
class DeviceDataHistoryAdmin(ImportExportModelAdmin):
    resource_class = DeviceDataHistoryResource 
    skip_admin_csv_import_button = True
    # exclude_buttons = ['import'] 

    # Manter os campos que você quer ver rapidamente
    list_display = ('device', 'timestamp', 'get_temperature_celsius', 'get_humidity_percent', 'get_all_data_summary') 
    list_filter = ('device__location', 'device__device_type', 'timestamp') 
    search_fields = ('device__name', 'device__device_id', 'data_payload')
    readonly_fields = ('device', 'data_payload_pretty_print', 'timestamp') 
    date_hierarchy = 'timestamp'

    # Métodos para extrair e exibir dados específicos do JSONField (se for comum)
    def get_temperature_celsius(self, obj):
        return obj.data_payload.get('temperature_celsius', 'N/A')
    get_temperature_celsius.short_description = 'Temperatura (°C)'
    get_temperature_celsius.admin_order_field = 'data_payload__temperature_celsius'

    def get_humidity_percent(self, obj):
        return obj.data_payload.get('humidity_percent', 'N/A')
    get_humidity_percent.short_description = 'Umidade (%)'
    get_humidity_percent.admin_order_field = 'data_payload__humidity_percent'

    # def get_relay_state_D1(self, obj):
    #     return obj.data_payload.get('relay_state_D1', 'N/A')
    # get_relay_state_D1.short_description = 'Relé D1'
    # get_relay_state_D1.admin_order_field = 'data_payload__relay_state_D1'

    # NOVO: Método para exibir um resumo dos dados no list_display
    def get_all_data_summary(self, obj):
        # Transforma o JSON em uma string legível para a tabela
        return str(obj.data_payload) 
    get_all_data_summary.short_description = 'Todos os Dados'
    
    # NOVO: Método para exibir o JSON formatado na tela de detalhes do objeto
    # Isso melhora a visualização do JSON completo
    def data_payload_pretty_print(self, obj):
        return format_html('<pre>{}</pre>', json.dumps(obj.data_payload, indent=2))
    data_payload_pretty_print.short_description = 'Dados Recebidos (JSON)'




