
# devices/serializers.py
from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        # AGORA SÓ OS CAMPOS QUE SEMPRE SÃO SOMENTE LEITURA
        read_only_fields = ('last_seen', 'is_online', 'created_at') 
        # 'last_command', 'last_command_at' e 'pending_command' agora podem ser escritos



"""# devices/serializers.py
from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__' # Inclui todos os campos do modelo Device
        read_only_fields = ('last_seen', 'is_online', 'created_at', 'last_command', 'last_command_at')"""

