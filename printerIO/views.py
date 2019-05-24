from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework_extensions.mixins import NestedViewSetMixin
from printerIO.serializers import *
from printerIO.models import *
from printerIO.selectors import get_queues, get_queue
from printerIO.services import create_queue, delete_queue


class PrintingModelViewSet(viewsets.ModelViewSet):
    queryset = PrintingModel.objects.all()
    serializer_class = PrintingModelSerializer


class PrinterViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class QualityViewSet(viewsets.ModelViewSet):
    queryset = PrintedModelQuality.objects.all()
    serializer_class = PrintingQualitySerializer


class QueuesListApi(APIView):
    authentication_classes = (BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk=None):
        queues = get_queues({'parent_lookup_printer':pk})
        data = QueueSerializer(queues, many=True)
        return Response(data.data, status=status.HTTP_200_OK)


class QueueCreateApi(CreateAPIView):
    permission_classes = (AllowAny,)

    class InputSerializer(serializers.Serializer):
        printing_models_id = serializers.PrimaryKeyRelatedField(source='printing_models',
                                                                write_only=True,
                                                                many=True,
                                                                queryset=PrintingModel.objects.all(),
                                                                help_text="Ids of models you want to add to the queue")

    def get_serializer(self):
        return self.InputSerializer()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        print(serializer.is_valid())
        print(serializer.validated_data)

        return Response(status=status.HTTP_202_ACCEPTED)


class TestingQueueViewSet(NestedViewSetMixin, viewsets.GenericViewSet):


    def list(self, request, *args, **kwargs):
        queryset = get_queues(kwargs)
        serializer = QueueSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = QueueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_queue(**serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        queue = get_queue(kwargs['pk'])
        delete_queue(queue)

        return Response("deleted", status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):
        pass
