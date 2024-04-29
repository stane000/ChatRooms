from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import Room, User
from .serializers import RoomSerializer, UserSerializer
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/users/:password',
        'DELETE /api/delete_user/:id',
        'DELETE /api/delete_room/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    logger.info("usloo")
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    rooms = Room.objects.get(pk=pk)
    serializer = RoomSerializer(rooms)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteRoom(request, pk):
    try:
        room = Room.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "Room does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    room.delete()
    return Response({"message": "Room deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getUsers(request, key):
    if key == "ovojezaporka":
        rooms = User.objects.all()
        serializer = UserSerializer(rooms, many=True)
        return Response(serializer.data)
    else:
        return Response({"Wrong Password"})

@api_view(['DELETE'])
def deleteUser(request, pk, key):
    if key == "ovojezaporka":
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"Wrong Password"})
