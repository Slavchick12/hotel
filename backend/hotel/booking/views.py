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

    @action(detail=False, permission_classes=[AllowAny])
    def free_rooms(self, request):
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        result = (
            Reserve.objects.filter(start_date__lte=start_date, end_date__gte=end_date) |
            Reserve.objects.filter(start_date__gte=start_date, start_date__lt=end_date) |
            Reserve.objects.filter(end_date__lte=start_date, end_date__gte=end_date)
        )
        queryset = self.get_queryset().exclude(room__in=result)
        context = {'request': request}
        serializer = self.get_serializer(queryset, context=context, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


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
