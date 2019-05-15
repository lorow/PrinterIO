from rest_framework import viewsets
from printerIO.serializers import *
from printerIO.models import *


class PrintingModelViewSet(viewsets.ModelViewSet):
    queryset = PrintingModel.objects.all()
    serializer_class = PrintingModelSerializer


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class QueueViewSet(viewsets.ModelViewSet):
    view_name = "QueueViewSet"
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
