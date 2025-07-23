#iot_monitor_project/__init__.py

# Este irá garantir que o app do Celery seja sempre importado quando o Django iniciar,
# então as tarefas compartilhadas podem ser usadas.
from .celery import app as celery_app

__all__ = ('celery_app',)