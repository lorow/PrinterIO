from typing import Iterable
from printerIO.models import Queue, Printer, PrintingModel


def get_models() -> Iterable[PrintingModel]:
    return PrintingModel.objects.all()


def get_model(model_id: int) -> PrintingModel:
    return PrintingModel.objects.get(pk=model_id)


def get_printers() -> Iterable[Printer]:
    return Printer.objects.all()


def get_printer(printer_id: int) -> Printer:
    return Printer.objects.get(id=printer_id)


def get_queues(printer_id: int = None) -> Iterable[Queue]:
    if printer_id:
        return Queue.objects.filter(printer=printer_id)
    return Queue.objects.all().prefetch_related('printing_models')


def get_queue_by_printer(printer_id: int) -> Queue:
    return Queue.objects.get(printer=printer_id)


def get_queue_by_queueID(queue_id: int) -> Queue or None:
    return Queue.objects.get(pk=queue_id)
