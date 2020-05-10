from printerIO.models import Queue, Printer

# from printerIO.apps import PrinterIOConfig
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .serializers import QueueSerializer
import django_filters


class QueueViewset(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ("printer",)

    def handle_printer_id(self, request, **kwargs):
        # due to the way drf-nested handles the routing
        # we have to manually add the printer param
        # so that the drf knows what's up

        if "printer" not in request.data:
            request.data["printer"] = get_object_or_404(
                Printer, pk=kwargs["printers_pk"]
            )

        return request

    def create(self, request, *args, **kwargs):
        req = self.handle_printer_id(request, kwargs)
        # PrinterIOConfig.printing_manager.get_new_queue(queue, queue.printer)
        return super().create(request=req, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        req = self.handle_printer_id(request, kwargs)
        # PrinterIOConfig.printing_manager.get_new_queue(queue, queue.printer)
        return super().update(request=req, *args, **kwargs)
