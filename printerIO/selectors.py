from typing import Iterable
from printerIO.models import Queue


def get_queues() -> Iterable[Queue]:
    return Queue.objects.all().prefetch_related('printing_models')


def get_queue(queue_id) -> Queue:
    return Queue.objects.get(pk=queue_id)
