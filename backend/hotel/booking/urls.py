from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReserveViewSet, RoomViewSet

router_v1 = DefaultRouter()
router_v1.register('rooms', RoomViewSet, basename='rooms')
router_v1.register('reserves', ReserveViewSet, basename='reserves')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
