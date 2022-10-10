from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Reserve, Room
from .permisions import IsAdminOrReadOnlyPermission
from .serializers import ReserveSerializer, RoomSerializer
from .utils import date_format_test, free_rooms


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    permission_classes = [IsAdminOrReadOnlyPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter
    )
    filterset_fields = ('cost', 'place_quantity')
    ordering_fields = ('cost', 'place_quantity')
    ordering = ('cost',)

    def get_queryset(self):
        queryset = super().get_queryset()
        get_params = self.request.GET
        start_date = get_params.get('start_date')
        end_date = get_params.get('end_date')
        if (start_date is not None and end_date is not None and date_format_test(start_date)
           and date_format_test(end_date)):
            return free_rooms(start_date, end_date)
        return queryset

    def get_serializer_class(self):
        return RoomSerializer


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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
