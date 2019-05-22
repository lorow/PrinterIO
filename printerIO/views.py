from rest_framework import viewsets
from printerIO.serializers import *
from printerIO.models import *
from printerIO.selectors import get_queues, get_queue
from printerIO.services import create_queue
from rest_framework.response import Response
from rest_framework import status
from rest_framework_extensions.mixins import NestedViewSetMixin


class PrintingModelViewSet(viewsets.ModelViewSet):
    queryset = PrintingModel.objects.all()
    serializer_class = PrintingModelSerializer


class PrinterViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class QualityViewSet(viewsets.ModelViewSet):
    queryset = PrintedModelQuality.objects.all()
    serializer_class = PrintingQualitySerializer


class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

    def list(self, request, *args, **kwargs):
        queues = Queue.objects.filter(printer=kwargs['parent_lookup_printer'])
        serializer = QueueSerializer(queues, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queue = get_queue(queue_id=kwargs['pk'])
        data = QueueSerializer(queue)
        return Response(data.data)

    def create(self, request, *args, **kwargs):

        serializer = QueueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_queue(**serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TestingQueueViewSet(NestedViewSetMixin, viewsets.GenericViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

    def list(self, request, *args, **kwargs):
        queryset = Queue.objects.filter(printer=kwargs['parent_lookup_printer'])
        serializer = QueueSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Endpoint that allows you to create an queue
            :Params
            : printing_models: list(int)
        """
        serializer = QueueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_queue(**serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        pass
