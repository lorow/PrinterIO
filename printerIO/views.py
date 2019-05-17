from rest_framework import viewsets
from rest_framework.views import APIView
from printerIO.serializers import *
from printerIO.models import *
from printerIO.selectors import get_queues
from rest_framework import response


class PrintingModelViewSet(viewsets.ModelViewSet):
    queryset = PrintingModel.objects.all()
    serializer_class = PrintingModelSerializer


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class QueueList(APIView):
    queryset = Queue.objects.all()  # due to permissions

    def get(self, request):
        queues = get_queues()
        serializer = QueueSerializer(queues, many=True)
        return response.Response(serializer.data)
