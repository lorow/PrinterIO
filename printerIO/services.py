from printerIO.models import Queue, Printer
from typing import List


def create_queue(printer: int, printing_models: List) -> Queue:
    printer_object = Printer.objects.get(id=printer)
    queue = Queue.objects.create(printer=printer_object)
    queue.printing_models.set(printing_models)
    queue.save()

    return queue


def delete_queue(queue: Queue) -> None:
    queue.delete()
