from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Reserve, Room
from .permisions import IsAdminOrReadOnlyPermission
from .serializers import ReserveSerializer, RoomSerializer

ROOM_RESERVED_EXIST = 'Данная комната уже забронирована'
RESERVE_DELETED_OK = 'Бронь данной комнаты успешно удалена'
ROOM_IS_NOT_EXIST = 'Данной комнаты не существует'
CANNOT_DELETE_NOT_YOUR_RESERVE = ('Данной брони не существует, либо нельзя '
                                  'удалить чужую бронь')


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter
    )
    filterset_fields = ('cost', 'place_quantity')
    ordering_fields = ('cost', 'place_quantity')
    ordering = ('cost',)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def my_reserves(self, request):
        serializer = ReserveSerializer(
            Reserve.objects.filter(user=request.user),
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated]
    )
    def reserve(self, request, pk):
        try:
            room = get_object_or_404(Room, id=pk)
        except Exception:
            return Response(
                {'errors': ROOM_IS_NOT_EXIST},
                status.HTTP_404_NOT_FOUND
            )
        if Reserve.objects.filter(room=room).exists():
            return Response(
                {'errors': ROOM_RESERVED_EXIST},
                status.HTTP_400_BAD_REQUEST
            )
        reserve = Reserve.objects.create(
            user=request.user,
            room=room,
            date=request.data['date']
        )
        Room.objects.filter(id=pk).update(free=False)
        serializer = ReserveSerializer(
            reserve,
            context={'request': request}
        )
        return Response(serializer.data, status.HTTP_201_CREATED)

    @reserve.mapping.delete
    def delete_reserve(self, request, pk):
        try:
            room = get_object_or_404(Room, id=pk)
        except Exception:
            return Response(
                {'errors': ROOM_IS_NOT_EXIST},
                status.HTTP_404_NOT_FOUND
            )
        try:
            if request.user.is_superuser:
                reserve = get_object_or_404(
                    Reserve,
                    room=room
                )
            else:
                reserve = get_object_or_404(
                    Reserve,
                    user=request.user,
                    room=room
                )
        except Exception:
            return Response(
                {'errors': CANNOT_DELETE_NOT_YOUR_RESERVE},
                status.HTTP_404_NOT_FOUND
            )
        reserve.delete()
        Room.objects.filter(id=pk).update(free=True)
        return Response(
            {'ok': RESERVE_DELETED_OK},
            status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False,
        permission_classes=[AllowAny]
    )
    def free_rooms(self, request):
        serializer = RoomSerializer(
            Room.objects.filter(free=True),
            context={'request': request},
            many=True
        )
        return Response(
            serializer.data,
            status.HTTP_204_NO_CONTENT
        )
