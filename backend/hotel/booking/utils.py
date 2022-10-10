from datetime import datetime as dt

from .models import Reserve, Room


def free_rooms(start_date, end_date):
    not_free_rooms = (
        Reserve.objects.filter(start_date__lte=start_date, end_date__gte=end_date)
        | Reserve.objects.filter(start_date__gte=start_date, start_date__lt=end_date)
        | Reserve.objects.filter(end_date__lte=start_date, end_date__gte=end_date)
    )
    queryset = Room.objects.exclude(room__in=not_free_rooms)
    return queryset


def date_format_test(string):
    try:
        return bool(dt.strptime(string, '%Y-%m-%d'))
    except Exception:
        return False
