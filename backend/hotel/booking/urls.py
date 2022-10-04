from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RoomViewSet

router_v1 = DefaultRouter()
router_v1.register('rooms', RoomViewSet, basename='rooms')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
