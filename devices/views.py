#from django.shortcuts import render


# devices/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone # Para lidar com fusos horários
from .models import Device
from .serializers import DeviceSerializer

class DeviceAPIView(APIView):
    """
    View para criar ou atualizar um dispositivo IoT e receber seus dados.
    """
    def post(self, request, *args, **kwargs):
        device_id = request.data.get('device_id') # Pega o device_id do JSON enviado

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
        except Device.DoesNotExist:
            # Se o dispositivo não existir, cria um novo
            serializer = DeviceSerializer(data=request.data)
            is_new_device = True

        if serializer.is_valid():
            # Atualiza last_seen e is_online no momento da requisição
            # Isso garante que o status online seja baseado na última comunicação
            serializer.validated_data['last_seen'] = timezone.now()
            serializer.validated_data['is_online'] = True
            
            device_instance = serializer.save()

            # Retorna 201 Created se for um novo dispositivo, 200 OK se for atualização
            response_status = status.HTTP_201_CREATED if is_new_device else status.HTTP_200_OK
            return Response(serializer.data, status=response_status)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    



