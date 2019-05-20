from printerIO.models import Queue, Printer, PrintingModel
from typing import List

def create_queue(printer: Printer, printing_models: List):
    queue = Queue.objects.create(printer=printer)
    queue.printing_models.set(printing_models)
    queue.save()