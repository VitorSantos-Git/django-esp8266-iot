# devices/models.py
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Device(models.Model):
    device_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("ID do Dispositivo"), # Added verbose_name here
        help_text=_("ID único do dispositivo ESP8266 (ex: ESP8266_B001)")
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Nome Amigável"),
        help_text=_("Nome descritivo para o dispositivo (ex: Sensor Sala)")
    )
    device_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Tipo de Dispositivo"),
        help_text=_("Categoria do dispositivo (ex: Temperatura, Relé, IR)")
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Localização"),
        help_text=_("Onde o dispositivo está localizado (ex: Sala, Quarto)")
    )

    last_seen = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Última Conexão"),
        help_text=_("Data e hora da última comunicação do dispositivo")
    )
    is_online = models.BooleanField(
        default=False,
        verbose_name=_("Online"),
        help_text=_("Indica se o dispositivo está online")
    )

    data = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("Dados Recebidos"),
        help_text=_("Dados genéricos recebidos do dispositivo (temperatura, umidade, etc.)")
    )

    last_command = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Último Comando Executado"),
        help_text=_("O último comando que o dispositivo executou.")
    )
    last_command_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Executado Em"),
        help_text=_("Data e hora em que o último comando foi executado pelo dispositivo.")
    )

    pending_command = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("Comando Pendente"),
        help_text=_("Comando a ser enviado para o dispositivo (JSON: {'action': 'ligar', 'target': 'rele'})")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Criado Em"),
        help_text=_("Data e hora de criação do registro do dispositivo")
    )

    class Meta:
        verbose_name = _("Dispositivo")
        verbose_name_plural = _("Dispositivos")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.device_id})"


class ScheduledCommand(models.Model):
    # Traduzindo as escolhas dos dias da semana
    DAY_CHOICES = [
        (0, _('Sunday')),
        (1, _('Monday')),
        (2, _('Tuesday')),
        (3, _('Wednesday')),
        (4, _('Thursday')),
        (5, _('Friday')),
        (6, _('Saturday')),
    ]

    name = models.CharField(max_length=255, verbose_name=_("Nome do Comando"), help_text=_("Nome descritivo para o agendamento (ex: Ligar Luz da Sala)")) # Added verbose_name

    devices = models.ManyToManyField(Device, related_name='scheduled_commands',
                                     verbose_name=_("Dispositivos"), # Added verbose_name
                                     help_text=_("Selecione os dispositivos que receberão este comando."))

    command_json = models.JSONField(
        verbose_name=_("Comando JSON"), # Added verbose_name
        help_text=_("Comando a ser enviado no formato JSON (ex: {\"action\": \"ligar_rele\", \"target\": \"rele_D1\", \"value\": 1})"),
    )

    schedule_type = models.CharField(
        max_length=50,
        choices=[
            ('daily', _('Daily')),
            ('weekly', _('Weekly')),
            ('once', _('Once'))
        ],
        default='weekly',
        verbose_name=_("Tipo de Agendamento"), # Added verbose_name
        help_text=_("Tipo de agendamento: Diário (todos os dias), Semanal (dias específicos), Uma Vez (data e hora únicas).")
    )

    day_of_week = models.ManyToManyField(
        'DayOfWeek',
        blank=True,
        verbose_name=_("Dia da Semana"), # Added verbose_name
        help_text=_("Selecione os dias da semana para agendamentos semanais.")
    )

    time_of_day = models.TimeField(blank=True, null=True, verbose_name=_("Hora do Dia"), help_text=_("Hora (HH:MM:SS) para o comando ser enviado.")) # Added verbose_name

    run_once_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Executar Uma Vez Em"), help_text=_("Data e hora para executar o comando apenas uma vez.")) # Added verbose_name

    is_active = models.BooleanField(default=True, verbose_name=_("Ativo"), help_text=_("Marque para ativar o agendamento.")) # Added verbose_name
    last_triggered_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Última Execução"), help_text=_("Data e hora da última vez que este agendamento foi acionado.")) # Added verbose_name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Comando Agendado")
        verbose_name_plural = _("Comandos Agendados")
        ordering = ['name']

class DayOfWeek(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=_("Nome")) # Added verbose_name
    numeric_value = models.IntegerField(unique=True, verbose_name=_("Valor Numérico"), choices=ScheduledCommand.DAY_CHOICES) # Added verbose_name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Dia da Semana")
        verbose_name_plural = _("Dias da Semana")
        ordering = ['numeric_value']