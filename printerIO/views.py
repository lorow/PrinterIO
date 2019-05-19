from rest_framework import viewsets
from rest_framework.views import APIView
from printerIO.serializers import *
from printerIO.models import *
from printerIO.selectors import get_queues, get_queue
from rest_framework.response import Response


class PrintingModelViewSet(viewsets.ModelViewSet):
    queryset = PrintingModel.objects.all()
    serializer_class = PrintingModelSerializer


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class QualityViewSet(viewsets.ModelViewSet):
    queryset = PrintedModelQuality.objects.all()
    serializer_class = PrintingQualitySerializer


class QueueListApi(APIView):
    """An endpoint responsible for listing all running queues"""

    queryset = Queue.objects.all()  # due to permissions

    def get(self, request):
        queues = get_queues()
        serializer = QueueSerializer(queues, many=True)
        return Response(serializer.data)


class QueueDetailApi(APIView):
    """endpoint for listing details of one specific queue"""

    queryset = Queue.objects.all()

    def get(self, request, pk):
        queue = get_queue(queue_id=pk)
        data = QueueSerializer(queue)
        return Response(data.data)

