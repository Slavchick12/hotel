from django.db import models

from users.models import User


class Room(models.Model):
    number = models.SmallIntegerField(
        'Номер',
        unique=True,
        help_text='Номер комнаты'
    )
    cost = models.IntegerField(
        'Стоимость',
        default=0,
        help_text='Стоимость/сут.',
    )
    place_quantity = models.SmallIntegerField(
        'Количество мест',
        default=1,
        help_text='Количество мест'
    )
    free = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'комната'
        verbose_name_plural = 'комнаты'


class Reserve(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reserved_user'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='room',
        verbose_name='комната'
    )
    date = models.DateField(
        'дата',
    )

    class Meta:
        verbose_name = 'бронь'
        verbose_name_plural = 'брони'
