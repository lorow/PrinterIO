from rest_framework import viewsets
from printerIO.serializers import *
from printerIO.models import *
from rest_framework import response


class PrintingModelViewSet(viewsets.ModelViewSet):
    queryset = PrintingModel.objects.all()
    serializer_class = PrintingModelSerializer


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
