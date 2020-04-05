from printerIO.utils import flatten_list
from printerIO.models import Queue, Printer, PrintingModel
from collections import OrderedDict
from typing import Iterable


def create_queue(printer: int, printing_models: Iterable) -> Queue:
    """Service for creating queues"""
    printer_object = Printer.objects.get(id=printer)
    queue = Queue.objects.create(printer=printer_object)
    queue.printing_models.set(printing_models)
    queue.save()

    # since the queue's saved, let's notify our printing manager that it should make use of it
    # PrinterIOConfig.printing_manager.get_new_queue(queue, queue.printer)

    return queue


def delete_queue(queue: Queue) -> None:
    """Service that handles deletion of the queue"""
    queue.delete()


def add_models_to_queue(
    queue: Queue, models_to_add: Iterable[PrintingModel]
) -> Queue:
    """Service for adding models to the queue without re-adding existing ones"""
    for model in models_to_add:
        queue.printing_models.add(model.id)

    queue.save()

    # since the queue has been updated, we should let the printer manager know that something's changed
    # PrinterIOConfig.printing_manager.refresh_queue(queue, queue.printer)

    return queue


def remove_models_from_queue(
    queue: Queue, models_to_remove: Iterable[PrintingModel]
) -> Queue:
    """Service for removing given models from the queue"""
    for model in models_to_remove:
        queue.printing_models.remove(model.id)

    queue.save()

    # since the queue has been updated, we should let the printer manager know that something's changed
    # PrinterIOConfig.printing_manager.refresh_queue(queue, queue.printer)

    return queue
