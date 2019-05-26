from printerIO.models import Queue, Printer
from itertools import chain
from collections import OrderedDict


def create_queue(printer: int, printing_models: OrderedDict) -> Queue:
    printer_object = Printer.objects.get(id=printer)
    queue = Queue.objects.create(printer=printer_object)
    queue.printing_models.set(list(chain.from_iterable(printing_models.values())))
    queue.save()

    return queue


def delete_queue(queue: Queue) -> None:
    queue.delete()


def add_models_to_queue(queue: Queue, models_to_add: dict) -> Queue:
    for model in list(chain.from_iterable(models_to_add.values())):
        queue.printing_models.add(model.id)

    queue.save()
    return queue