from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from printerIO.serializers import *
from printerIO.models import *
from printerIO.selectors import get_queues, get_queue
from printerIO.services import create_queue, delete_queue, add_models_to_queue, remove_models_from_queue


class PrintingModelViewSet(viewsets.ModelViewSet):
    queryset = PrintingModel.objects.all()
    serializer_class = PrintingModelSerializer


class PrinterViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class QualityViewSet(viewsets.ModelViewSet):
    queryset = PrintedModelQuality.objects.all()
    serializer_class = PrintingQualitySerializer


class QueuesListApi(ListAPIView):
    def get(self, request, *args, **kwargs):
        queues = get_queues({'parent_lookup_printer': kwargs['printer_id']})
        data = QueueSerializer(queues, many=True)
        return Response(data.data, status=status.HTTP_200_OK)


class QueueCreateApi(CreateAPIView):
    class InputSerializer(serializers.Serializer):
        printing_models_ids = serializers.PrimaryKeyRelatedField(source='printing_models',
                                                                 write_only=True,
                                                                 many=True,
                                                                 queryset=PrintingModel.objects.all(),
                                                                 help_text="Ids of models you want to add to the queue")

    def get_serializer(self):
        return self.InputSerializer()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        if serializer.is_valid():
            try:
                create_queue(kwargs['printer_id'], serializer.validated_data)
                return Response(data={"status": "created successfully"},
                                status=status.HTTP_202_ACCEPTED)
            except Exception:
                return Response(data={"status": "printer with given ID does not exists or it already has a queue"},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueueDeleteApi(DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        queue = get_queue(kwargs['printer_id'])
        try:
            delete_queue(queue)
            return Response(data={"status": "The queue has been successfully deleted"},
                            status=status.HTTP_200_OK)
        except Exception:
            return Response(data={"status": "The queue you're trying to delete does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)


class AddModelsToQueueApi(APIView):
    """Lets you add one or more models to the existing queue, which is identified by the supplied printer_id"""

    class InputSerializer(serializers.Serializer):
        printing_model_ids = serializers.PrimaryKeyRelatedField(
            source='printing_models',
            write_only=True,
            many=True,
            queryset=PrintingModel.objects.all(),
            help_text="Id of an existing model you want to add to queue")

    def get_serializer(self):
        return self.InputSerializer()

    def patch(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)

        if serializer.is_valid():
            queue = get_queue(kwargs['printer_id'])
            add_models_to_queue(queue, serializer.validated_data)
            return Response(data={"status": "The models have been added successfully"}, status=status.HTTP_200_OK)

        return Response(data={"status": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class RemoveModelsFromQueueApi(APIView):
    """Lets you remove one or more models from the existing queue, which is identified by the supplied printer_id"""

    class InputSerializer(serializers.Serializer):
        printing_model_ids = serializers.PrimaryKeyRelatedField(
            source='printing_models',
            write_only=True,
            many=True,
            queryset=PrintingModel.objects.all(),
            help_text="Id of an existing model you want to add to queue")

    def get_serializer(self):
        return self.InputSerializer()

    def patch(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        if serializer.is_valid():
            queue = get_queue(kwargs['printer_id'])
            remove_models_from_queue(queue, serializer.validated_data)
            return Response(data={"status": "Models have been deleted successfully"})

        return Response(data={"status": "Given model or printer does not exist"}, )


class SwapPrintersInQueueApi(APIView):
    class InputSerializer(serializers.Serializer):
        printer_id = serializers.PrimaryKeyRelatedField(
            source='printer',
            write_only=True,
            many=False,
            queryset=Printer.objects.all(),
            help_text="ID of the printer you want this queue to be transferred to"
        )

    def patch(self, request, *args, **kwargs):
        return Response()
