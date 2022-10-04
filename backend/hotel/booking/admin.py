from django.contrib import admin
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Reserve, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'cost',
        'place_quantity'
    )
    search_fields = (
        'number',
        'cost',
        'place_quantity'
    )


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = (
        'room',
        'date',
    )
    search_fields = (
        'room',
        'date',
    )

    @receiver(post_delete)
    def signal_function_name(sender, instance, using, **kwargs):
        room = instance.room
        Room.objects.filter(id=room.id).update(free=True)
