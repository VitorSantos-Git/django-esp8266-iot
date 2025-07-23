#iot_monitor_project/celery.py
import os
from celery import Celery

# Define o módulo de configurações padrão do Django para o 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iot_monitor_project.settings')

app = Celery('iot_monitor_project')

# Usando uma string aqui significa que o worker não precisa
# serializar os objetos de configuração para processos filhos.
# namespace='CELERY' significa que todas as configurações relacionadas ao Celery
# devem ter um prefixo 'CELERY_' no seu arquivo settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre e carrega automaticamente as tarefas dos arquivos tasks.py em todas as apps Django registradas.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')