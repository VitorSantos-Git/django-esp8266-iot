# devices/models.py
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
#import json


"""# Função de validação para o campo JSONField
def validate_json_command(value):
    try:
        json.loads(value)
    except json.JSONDecodeError:
        raise ValidationError("O campo 'Comando JSON' deve ser um JSON válido.")
"""


class Device(models.Model):
    # Campos de identificação e status do dispositivo
    device_id = models.CharField(
        max_length=100, 
        unique=True, 
        help_text="ID único do dispositivo ESP8266 (ex: ESP8266_B001)"
    )
    name = models.CharField(
        max_length=100, 
        verbose_name="Nome Amigável", 
        help_text="Nome descritivo para o dispositivo (ex: Sensor Sala)"
    )
    device_type = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="Tipo de Dispositivo",
        help_text="Categoria do dispositivo (ex: Temperatura, Relé, IR)"
    )
    location = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Localização",
        help_text="Onde o dispositivo está localizado (ex: Sala, Quarto)"
    )
    
    # Campos para monitoramento de status
    last_seen = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última Conexão",
        help_text="Data e hora da última comunicação do dispositivo"
    )
    is_online = models.BooleanField(
        default=False, 
        verbose_name="Online",
        help_text="Indica se o dispositivo está online"
    )

    # Campo para armazenar dados genéricos em JSON
    data = models.JSONField(
        blank=True, 
        null=True, 
        verbose_name="Dados Recebidos",
        help_text="Dados genéricos recebidos do dispositivo (temperatura, umidade, etc.)"
    )

    # Campo para armazenar último comando
    last_command = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Último Comando Executado", 
        help_text="O último comando que o dispositivo executou."
    )
    last_command_at = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name="Executado Em", 
        help_text="Data e hora em que o último comando foi executado pelo dispositivo."
    )

    # Campo para armazenar o comando que precisa ser enviado
    pending_command = models.JSONField(
        blank=True, 
        null=True, 
        verbose_name="Comando Pendente",
        help_text="Comando a ser enviado para o dispositivo (JSON: {'action': 'ligar', 'target': 'rele'})"
    )

    # Timestamp de criação do dispositivo no sistema
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Criado Em",
        help_text="Data e hora de criação do registro do dispositivo"
    )

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.device_id})"
    

class ScheduledCommand(models.Model):
    DAY_CHOICES = [
        (0, 'Domingo'),
        (1, 'Segunda-feira'),
        (2, 'Terça-feira'),
        (3, 'Quarta-feira'),
        (4, 'Quinta-feira'),
        (5, 'Sexta-feira'),
        (6, 'Sábado'),
    ]   

    name = models.CharField(max_length=255, help_text="Nome descritivo para o agendamento (ex: Ligar Luz da Sala)")
    
    # Relação Many-to-Many com Device, para que um agendamento possa afetar múltiplos dispositivos
    devices = models.ManyToManyField(Device, related_name='scheduled_commands', 
                                     help_text="Selecione os dispositivos que receberão este comando.")
    
    command_json = models.JSONField(
        help_text="Comando a ser enviado no formato JSON (ex: {\"action\": \"ligar_rele\", \"target\": \"rele_D1\", \"value\": 1})",
        #validators=[validate_json_command] # Adiciona validação para JSON válido
    )
    
    # Opções de agendamento
    schedule_type = models.CharField(
        max_length=50, 
        choices=[('daily', 'Diário'), ('weekly', 'Semanal'), ('once', 'Uma Vez')],
        default='weekly',
        help_text="Tipo de agendamento: Diário (todos os dias), Semanal (dias específicos), Uma Vez (data e hora únicas)."
    )
    
    # Para agendamentos semanais
    day_of_week = models.ManyToManyField(
        'DayOfWeek',
        blank=True,
        help_text="Selecione os dias da semana para agendamentos semanais."
    )
    
    # Hora do dia para agendamentos diários/semanais
    time_of_day = models.TimeField(blank=True, null=True, help_text="Hora (HH:MM:SS) para o comando ser enviado.")

    # Para agendamentos de uma vez (data e hora específicas)
    run_once_at = models.DateTimeField(blank=True, null=True, help_text="Data e hora para executar o comando apenas uma vez.")
    
    is_active = models.BooleanField(default=True, help_text="Marque para ativar o agendamento.")
    last_triggered_at = models.DateTimeField(blank=True, null=True, help_text="Data e hora da última vez que este agendamento foi acionado.")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Comando Agendado"
        verbose_name_plural = "Comandos Agendados"
        ordering = ['name']

# Modelo auxiliar para os dias da semana
class DayOfWeek(models.Model):
    name = models.CharField(max_length=20, unique=True)
    numeric_value = models.IntegerField(unique=True, choices=ScheduledCommand.DAY_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dia da Semana"
        verbose_name_plural = "Dias da Semana"
        ordering = ['numeric_value']
