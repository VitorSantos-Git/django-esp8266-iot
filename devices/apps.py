from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _ # Importe gettext_lazy



class DevicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devices'
    verbose_name = _("Dispositivos") 
