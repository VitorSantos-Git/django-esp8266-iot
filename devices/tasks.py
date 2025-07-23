#devices/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Device, ScheduledCommand, DayOfWeek
import json
import logging

logger = logging.getLogger(__name__)

@shared_task
def debug_task_example(message):
    """
    Uma tarefa de depuração simples para testar a configuração do Celery Beat.
    """
    logger.info(f"Debug Task Executed: {message} at {timezone.now()}")
    print(f"Debug Task Executed: {message} at {timezone.now()}")


@shared_task
def send_scheduled_command_to_device(device_id, command_json):
    """
    Tarefa para enviar um comando agendado para um dispositivo específico.
    Esta tarefa será chamada pelo Celery Beat.
    """
    try:
        device = Device.objects.get(device_id=device_id)
        
        # Atualiza o campo pending_command do dispositivo
        device.pending_command = json.loads(command_json) # Converte a string JSON de volta para dict
        device.save(update_fields=['pending_command'])
        
        logger.info(f"Comando agendado '{command_json}' enviado para o dispositivo '{device_id}'")
        print(f"Comando agendado '{command_json}' enviado para o dispositivo '{device_id}'")

    except Device.DoesNotExist:
        logger.error(f"Dispositivo com ID '{device_id}' não encontrado para comando agendado.")
    except json.JSONDecodeError:
        logger.error(f"Erro ao decodificar JSON do comando para o dispositivo '{device_id}': {command_json}")
    except Exception as e:
        logger.error(f"Erro inesperado ao enviar comando agendado para '{device_id}': {e}")


@shared_task
def check_and_dispatch_scheduled_commands():
    """
    Tarefa periódica que verifica os comandos agendados no banco de dados
    e enfileira as tarefas 'send_scheduled_command_to_device' quando devido.
    """
    now = timezone.localtime(timezone.now()) # Usa o fuso horário configurado no settings.py
    current_time = now.time()
    current_day_of_week_numeric = now.weekday() # Monday is 0 and Sunday is 6.

    logger.info(f"Verificando comandos agendados às {now.strftime('%H:%M:%S')} do dia {now.strftime('%A')}.")

    # Comandos Diários
    daily_commands = ScheduledCommand.objects.filter(
        is_active=True,
        schedule_type='daily',
        time_of_day__hour=current_time.hour,
        time_of_day__minute=current_time.minute
    ).exclude(last_triggered_at__date=now.date()) # Evita disparar múltiplas vezes no mesmo dia

    for command in daily_commands:
        for device in command.devices.all():
            send_scheduled_command_to_device.delay(device.device_id, json.dumps(command.command_json))
            logger.info(f"Disparando comando diário '{command.name}' para {device.device_id}")
        command.last_triggered_at = now
        command.save(update_fields=['last_triggered_at'])

    # Comandos Semanais
    # Ajusta o weekday do Python (0=Seg, ..., 6=Dom) para o seu modelo (0=Dom, ..., 6=Sáb)
    # Python's weekday: Monday is 0 and Sunday is 6.
    # Your model's DayOfWeek: Sunday is 0 and Saturday is 6.
    # So, if Python's weekday is 6 (Sunday), your model's numeric_value should be 0.
    # If Python's weekday is 0 (Monday), your model's numeric_value should be 1, etc.
    
    # Mapeamento: Python weekday (0-6) -> Seu DayOfWeek numeric_value (0-6)
    # Python: Seg(0) Ter(1) Qua(2) Qui(3) Sex(4) Sab(5) Dom(6)
    # Seu:    Dom(0) Seg(1) Ter(2) Qua(3) Qui(4) Sex(5) Sab(6)
    
    # Mapeamento para o seu modelo:
    # Se Python_weekday == 6 (Domingo), DayOfWeek_numeric_value = 0
    # Senão, DayOfWeek_numeric_value = Python_weekday + 1
    
    mapped_day_of_week_numeric = (current_day_of_week_numeric + 1) % 7 

    weekly_commands = ScheduledCommand.objects.filter(
        is_active=True,
        schedule_type='weekly',
        day_of_week__numeric_value=mapped_day_of_week_numeric,
        time_of_day__hour=current_time.hour,
        time_of_day__minute=current_time.minute
    ).exclude(last_triggered_at__date=now.date()) # Evita disparar múltiplas vezes no mesmo dia

    for command in weekly_commands:
        for device in command.devices.all():
            send_scheduled_command_to_device.delay(device.device_id, json.dumps(command.command_json))
            logger.info(f"Disparando comando semanal '{command.name}' para {device.device_id}")
        command.last_triggered_at = now
        command.save(update_fields=['last_triggered_at'])

    # Comandos Uma Vez
    # Filtra comandos que devem ser executados agora e ainda não foram
    once_commands = ScheduledCommand.objects.filter(
        is_active=True,
        schedule_type='once',
        run_once_at__lte=now, # Executar se a hora agendada for agora ou no passado
        last_triggered_at__isnull=True # Garante que só seja executado uma vez
    )
    
    for command in once_commands:
        for device in command.devices.all():
            send_scheduled_command_to_device.delay(device.device_id, json.dumps(command.command_json))
            logger.info(f"Disparando comando 'uma vez' '{command.name}' para {device.device_id}")
        command.last_triggered_at = now
        command.is_active = False # Desativa o comando após a execução única
        command.save(update_fields=['last_triggered_at', 'is_active'])

    logger.info("Verificação de comandos agendados concluída.")