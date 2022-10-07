from rest_framework import serializers
from rest_framework.response import Response
from .models import Reserve, Room
from rest_framework import status
RESERVE_EXIST = 'Бронь на данную комнату уже существует'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'number', 'cost', 'place_quantity')


class ReserveSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(source='room.number')

    class Meta:
        model = Reserve
        fields = ('number', 'date')

    def validate(self, data):
        id = data['room']['number']
        room = Room.objects.get(pk=id)
        if Reserve.objects.filter(room=room).exists():
            raise serializers.ValidationError(RESERVE_EXIST)
        return super().validate(data)

    def create(self, request, validated_data):
        print(request.user)
        user = request.user
        room = validated_data.pop('room')
        date = validated_data.pop('date')
        Reserve.objects.create(user=user, room=room, date=date)
        return validated_data
