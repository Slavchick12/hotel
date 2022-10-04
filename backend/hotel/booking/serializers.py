from rest_framework import serializers

from .models import Reserve, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'id',
            'number',
            'cost',
            'place_quantity',
            'free'
        )


class ReserveSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(source='room.number')

    class Meta:
        model = Reserve
        fields = (
            'number',
            'date'
        )
