from rest_framework import serializers
from chat.models import Room, Message
from polyclinic.serializers import UserSerializer

class RoomSerializer(serializers.ModelSerializer):
	member = UserSerializer(many=True, read_only=True)
	members = serializers.ListField(write_only=True)

	def create(self, validatedData):
		memberObject = validatedData.pop('members')
		room = Room.objects.create(**validatedData)
		room.member.set(memberObject)
		return room

	class Meta:
		model = Room
		exclude = ['id']

class MessageSerializer(serializers.ModelSerializer):
	userName = serializers.SerializerMethodField()
	userImage = serializers.ImageField(source='social.image')

	class Meta:
		model = Message
		exclude = ['id', 'chat']

	def get_userName(self, Obj):
		return Obj.user.first_name + ' ' + Obj.user.last_name
