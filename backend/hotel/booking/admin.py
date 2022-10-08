from django.contrib import admin

from .models import Reserve, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'cost', 'place_quantity')
    search_fields = ('number', 'cost', 'place_quantity')


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ('room', 'start_date', 'end_date')
    search_fields = ('room', 'start_date', 'end_date')
