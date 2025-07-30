# devices/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone # Para lidar com fusos horários
from .models import Device, DeviceDataHistory
from .serializers import DeviceSerializer
import json

class DeviceAPIView(APIView):
    """
    View para criar ou atualizar um dispositivo IoT e receber seus dados.
    """
    def post(self, request, *args, **kwargs):
        device_id = request.data.get('device_id') # Pega o device_id do JSON enviado

        # Campos que o ESP8266 envia para atualizar o dispositivo principal
        name = request.data.get('name')
        received_device_type = request.data.get('device_type') # 'type' no JSON do ESP é 'device_type' no Django
        location = request.data.get('location')
        received_data_payload = request.data.get('data') # <--- NOVO: O payload de dados do sensor/relé
        
        if not device_id:
            return Response(
                {"detail": "ID do dispositivo é obrigatório."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Tenta encontrar um dispositivo existente pelo device_id
            device = Device.objects.get(device_id=device_id)
            serializer = DeviceSerializer(device, data=request.data, partial=True)
            # partial=True permite que você atualize apenas alguns campos
            is_new_device = False

            data_changed = False
            if received_data_payload is not None and isinstance(received_data_payload, dict):
                if device.data is None or json.dumps(received_data_payload, sort_keys=True) != json.dumps(device.data, sort_keys=True):
                    data_changed = True
                    device.data = received_data_payload # Atualiza o último estado no Device principal
            
            # Atualiza outros campos do dispositivo se forem enviados
            device.name = name if name is not None else device.name
            device.device_type = received_device_type if received_device_type is not None else device.device_type
            device.location = location if location is not None else device.location
            device.is_online = True
            device.last_seen = timezone.now()
            device.save()

        except Device.DoesNotExist:
            # Se o dispositivo não existir, cria um novo
            device = Device.objects.create(
                device_id=device_id,
                name=name if name is not None else f"Dispositivo {device_id}", # Nome padrão se não for enviado
                type=received_device_type,
                location=location,
                is_online=True,
                last_seen=timezone.now()
            )
            is_new_device = True
            data_changed = True
        
        if data_changed and received_data_payload is not None and isinstance(received_data_payload, dict):
            DeviceDataHistory.objects.create(
                device=device,
                data_payload=received_data_payload,
                timestamp=timezone.now()
            )
            print(f"Dados históricos ALTERADOS e salvos para {device.device_id}: {received_data_payload}")
        elif not data_changed:
            print(f"Dados do dispositivo {device.device_id} NÃO ALTERADOS. Histórico não salvo.")
        elif received_data_payload is not None:
             print(f"Atenção: 'data' recebido para {device.device_id} não é um objeto JSON válido ou é None: {received_data_payload}")
    
        # Verifica se há dados no payload 'data' e os salva no histórico
        if received_data_payload is not None and isinstance(received_data_payload, dict):
            # Certifique-se de que o 'data' recebido do ESP8266 seja um dicionário (JSON object)
            DeviceDataHistory.objects.create(
                device=device,
                data_payload=received_data_payload,
                timestamp=timezone.now()
            )
            print(f"Dados históricos salvos para {device.device_id}: {received_data_payload}")
        elif received_data_payload is not None:
             # Se for um valor simples (não um objeto JSON), você pode lidar com isso de outra forma
             # Por exemplo, encapsulá-lo em um dicionário ou logar um aviso
             print(f"Atenção: 'data' recebido para {device.device_id} não é um objeto JSON: {received_data_payload}")

        # Lógica para enviar pending_command de volta para o dispositivo
        response_data = {'status': 'success'}
        if device.pending_command:
            response_data['command'] = device.pending_command
            # NÃO LIMPAR AQUI. O comando deve ser limpo SOMENTE APÓS a confirmação do PUT do ESP
            # device.pending_command = None
            # device.save(update_fields=['pending_command'])

        # Prepara a resposta, possivelmente usando o DeviceSerializer para o dispositivo atualizado
        # Não precisamos do serializer para o histórico aqui, pois é uma criação direta.
        serializer = DeviceSerializer(device) # Serialize a instância atualizada do dispositivo
        response_data.update(serializer.data) # Adiciona os dados do dispositivo à resposta

        response_status = status.HTTP_201_CREATED if is_new_device else status.HTTP_200_OK
        return Response(response_data, status=response_status)

    def get(self, request, device_id, *args, **kwargs):
            """
            Permite que um dispositivo (ESP8266) consulte se há um comando pendente.
            Endpoint: /api/device/<device_id>/
            """
            try:
                device = Device.objects.get(device_id=device_id)
            except Device.DoesNotExist:
                return Response(
                    {"detail": "Dispositivo não encontrado."}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Atualiza last_seen e is_online ao receber uma requisição GET também
            device.last_seen = timezone.now()
            device.is_online = True
            device.save(update_fields=['last_seen', 'is_online'])

            if device.pending_command:
                command = device.pending_command
                # Limpa o comando pendente APÓS o envio para o ESP
                # A confirmação de execução virá em um PUT separado.
                device.pending_command = None
                device.save(update_fields=['pending_command'])
                
                return Response(
                    {"status": "command_pending", "command": command}, 
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"status": "no_command"}, 
                    status=status.HTTP_200_OK
                )
    

     # PUT para o ESP confirmar execução de comando
    def put(self, request, device_id, *args, **kwargs):
        """
        Permite que um dispositivo (ESP8266) confirme a execução de um comando.
        Endpoint: /api/device/<device_id>/
        JSON esperado: {"last_command": "nome_do_comando", "last_command_at": "ISO_8601_datetime_string"}
        """
        try:
            device = Device.objects.get(device_id=device_id)
        except Device.DoesNotExist:
            return Response(
                {"detail": "Dispositivo não encontrado."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Usamos partial=True porque o ESP enviará apenas os campos de comando
        serializer = DeviceSerializer(device, data=request.data, partial=True)

        if serializer.is_valid():
            # O ESP enviará 'last_command' e 'last_command_at'
            # No PUT, o 'last_seen' e 'is_online' também podem ser atualizados
            serializer.validated_data['last_seen'] = timezone.now()
            serializer.validated_data['is_online'] = True
            serializer.validated_data['last_command_at'] = timezone.now() 
            
            device_instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



    



