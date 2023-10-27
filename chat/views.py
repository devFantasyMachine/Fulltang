from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from chat.serializers import  MessageSerializer, RoomSerializer
from chat.models import Room, Message

class RoomView(APIView):
	def get(self, request, userId):
		chatRooms = Room.objects.filter(member=userId)
		serializer = RoomSerializer(
			chatRooms, many=True, context={"request": request}
		)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = RoomSerializer(
			data=request.data, context={"request": request}
		)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessagesView(ListAPIView):
	serializer_class = MessageSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		roomId = self.kwargs['roomId']
		return Message.objects.\
			filter(room__roomId=roomId).order_by('-timestamp')
