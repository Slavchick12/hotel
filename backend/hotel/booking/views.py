from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Reserve, Room
from .permisions import IsAdminOrReadOnlyPermission
from .serializers import ReserveSerializer, RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter
    )
    filterset_fields = ('cost', 'place_quantity')
    ordering_fields = ('cost', 'place_quantity')
    ordering = ('cost',)

    def get_queryset(self):
        return Room.objects.all()

    def get_serializer_class(self):
        return RoomSerializer

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def reserve(self, request, pk):
        room = get_object_or_404(Room, id=pk)
        if Reserve.objects.filter(room=room).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        reserve = Reserve.objects.create(user=request.user, room=room, date=request.data['date'])
        context = {'request': request}
        serializer = ReserveSerializer(reserve, context=context)
        return Response(serializer.data, status.HTTP_201_CREATED)

    @reserve.mapping.delete
    def delete_reserve(self, request, pk):
        room = get_object_or_404(Room, id=pk)
        if request.user.is_superuser:
            reserve = get_object_or_404(Reserve, room=room)
        else:
            reserve = get_object_or_404(Reserve, user=request.user, room=room)
        reserve.delete()

    @action(detail=False, permission_classes=[AllowAny])
    def free_rooms(self, request):
        reserved = Reserve.objects.all()
        queryset = self.get_queryset().exclude(room__in=reserved)
        context = {'request': request}
        serializer = self.get_serializer(queryset, context=context, many=True)
        return Response(serializer.data, status.HTTP_204_NO_CONTENT)


class ReserveViewSet(viewsets.ModelViewSet):
    queryset = Reserve.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        return ReserveSerializer
