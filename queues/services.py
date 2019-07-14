from printerIO.utils import flatten_list
from printerIO.models import Queue, Printer
from printerIO.apps import PrinterIOConfig
from collections import OrderedDict


def create_queue(printer: int, printing_models: OrderedDict) -> Queue:
    """Service for creating queues"""
    printer_object = Printer.objects.get(id=printer)
    queue = Queue.objects.create(printer=printer_object)
    queue.printing_models.set(flatten_list(printing_models.values()))
    queue.save()

    # since the queue is save, let's notify our printing manager that it should make use of it
    PrinterIOConfig.printing_manager.get_new_queue(queue, queue.printer)

    return queue


def delete_queue(queue: Queue) -> None:
    """Service that handles deletion of the queue"""
    queue.delete()


def add_models_to_queue(queue: Queue, models_to_add: dict) -> Queue:
    """Service for adding models to the queue without re-adding existing ones"""
    for model in flatten_list(models_to_add.values()):
        queue.printing_models.add(model.id)

    queue.save()

    # since the queue has been updated, we should let the printer manager know that something's changed

    PrinterIOConfig.printing_manager.refresh_queue(queue, queue.printer)

    return queue


def remove_models_from_queue(queue: Queue, models_to_remove: dict) -> Queue:
    """Service for removing given models from the queue"""
    for model in flatten_list(models_to_remove.values()):
        queue.printing_models.remove(model.id)

    queue.save()

    # since the queue has been updated, we should let the printer manager know that something's changed

    PrinterIOConfig.printing_manager.refresh_queue(queue, queue.printer)

    return queue
