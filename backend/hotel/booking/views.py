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
    filterset_fields = ('cost', 'place_quantity')
    ordering_fields = ('cost', 'place_quantity')
    ordering = ('cost',)

    def get_queryset(self):
        return Room.objects.all()

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def get_serializer_class(self):
        return RoomSerializer

    @action(detail=False, permission_classes=[IsAuthenticated])
    def my_reserves(self, request):
        queryset = Reserve.objects.filter(user=request.user)
        context = {'request': request}
        serializer = ReserveSerializer(queryset, context=context, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[AllowAny])
    def free_rooms(self, request):
        print(request.POST)
        reserved = Reserve.objects.all()
        queryset = self.get_queryset().exclude(room__in=reserved)
        context = {'request': request}
        serializer = self.get_serializer(queryset, context=context, many=True)
        return Response(serializer.data, status.HTTP_204_NO_CONTENT)
