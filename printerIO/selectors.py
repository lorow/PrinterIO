from typing import Iterable
from printerIO.models import Queue


def get_queues() -> Iterable[Queue]:
    return Queue.objects.all().prefetch_related('printing_models')
