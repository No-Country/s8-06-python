from .models import Room, Message
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import RoomSerializer, MessageSerializer
from rest_framework import status
from aplications.authentication.models import User, Professional

# Create your views here

#Funcion que redirecciona a la sala de chat
class NewRoom(CreateAPIView):

    def create(self, request):
        #Identificamos al usuario
        usuario= self.request.query_params.get('usuario')
        user = User.objects.get(username = usuario) 
        #Identificamos al Professional
        Professional = self.request.query_params.get('Professional')
        user_prof = User.objects.get(username=Professional)
        prof = Professional.objects.get(usuario=user_prof)

        if Room.objects.filter(user=user,professional=prof).exists():
            #Si la sala existe lo redirecciona a la sala, enviando el nombre del usuario
            return HttpResponse('Ya existe una conversacion con este usuario')
        else:
            #En otro caso se crea una nueva sala
            new_room = Room.objects.create(name=usuario+'-'+Professional, user=user, professional=prof)
            new_room.save()
            #Se redirecciona a la nueva sala con el usuario
            return HttpResponse('Sala creada exitosamente')

#MOSTRAR INFORMACION DE UNA SALA
class ShowRoom(APIView):
    def get(self, request):
        id_room = self.request.query_params.get('id_room')
        room = Room.objects.get(id=id_room)
        if( room is not None):  
            room_serializer = RoomSerializer(room)
            return Response(room_serializer.data,status=status.HTTP_200_OK)

        return Response({"message":"No se encontro la sala especificada"},status=status.HTTP_404_NOT_FOUND)

#MOSTRAR SALAS QUE TIENEN UN USUARIO
class ShowRoomsUser(APIView):
    def get(self, request):
        user_name= self.request.query_params.get('user_name')
        type_user = self.request.query_params.get('type_user')

        if type_user == 'Professional':
            user = User.objects.get(username=user_name)
            prof = Professional.objects.get(usuario=user)
            user_rooms= Room.objects.filter(professional=user, state=not(False)) #No mostrar aquellos suspendidos
        else:
            user = User.objects.get(username = user_name)
            user_rooms= Room.objects.filter(user=user, state=not(False)) #No mostrar aquellos suspendidos
        
        list_rooms= RoomSerializer(user_rooms, many=True)

        if len(list_rooms.data)!=0:
            return Response(list_rooms.data, status=status.HTTP_200_OK)
        return Response({"message":"El usuario especificado no tiene salas de chat"},status=status.HTTP_204_NO_CONTENT)

#VISTA QUE CREA LOS MENSAJES CUANDO SON ENVIADOS

class SendMessage(CreateAPIView):
    serializer_class = MessageSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            return HttpResponse('El mensaje se envio correctamente')
        except Exception as e:
            return HttpResponse('Error al enviar el mensaje, vuelva a intentarlo')

#VISTA PARA MOSTRAR LOS MENSAJES DE UNA SALA
class ShowListMessages(APIView):
    def get(self, reques):
        id_room = self.request.query_params.get('id_room')
        message_room = Message.objects.filter(room_id=id_room)
        list_message = MessageSerializer(message_room, many = True)

        if len(list_message.data)!=0:
            return Response(list_message.data, status=status.HTTP_200_OK)
        return Response({"message":"No se encontraron mensajes se la sala"},status=status.HTTP_204_NO_CONTENT)