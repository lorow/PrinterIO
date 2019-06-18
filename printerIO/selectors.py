from printerIO.models import Queue, Printer, PrintingModel
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from typing import Iterable


def get_models() -> Iterable[PrintingModel]:
    return PrintingModel.objects.all()


def get_model(model_id: int) -> PrintingModel:
    return PrintingModel.objects.get(pk=model_id)


def get_printers() -> Iterable[Printer]:
    return Printer.objects.all()


def get_printer(printer_id: int) -> Printer:
    return Printer.objects.get(id=printer_id)


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