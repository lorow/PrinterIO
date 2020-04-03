from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from printerIO.models import Queue


def get_queue_by_printer_id(printer_id: int) -> Queue:
    try:
        return Queue.objects.get(printer=printer_id)
    except ObjectDoesNotExist:
        raise ValidationError("This queue does not exist")


def get_queue_by_queue_id(queue_id: int) -> Queue or None:
    try:
        return Queue.objects.get(pk=queue_id)
    except ObjectDoesNotExist:
        raise ValidationError("This queue does not exist")
    