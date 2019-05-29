from typing import Iterable
from printerIO.models import Queue, Printer


def get_printers() -> Iterable[Printer]:
    return Printer.objects.all()

def get_printer(printer_id: int) -> Printer:
    return Printer.objects.get(id=printer_id)


def get_queues(queue_parameters=None) -> Iterable[Queue]:
    if queue_parameters:
        return Queue.objects.filter(printer=queue_parameters['parent_lookup_printer'])
    return Queue.objects.all().prefetch_related('printing_models')


def get_queue(queue_id: int) -> Queue:
    return Queue.objects.get(pk=queue_id)
