# devices/models.py
from django.db import models

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