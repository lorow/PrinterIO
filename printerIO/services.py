from printerIO.models import Queue, Printer
from typing import List


def create_queue(printer: Printer, printing_models: List) -> Queue:
    queue = Queue.objects.create(printer=printer)
    queue.printing_models.set(printing_models)
    queue.save()

    return queue