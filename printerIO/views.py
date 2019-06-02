from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from printerIO.serializers import *
from printerIO.models import *
from printerIO.selectors import *
from printerIO.services import *


class PrintingModelViewSet(viewsets.ModelViewSet):
    queryset = PrintingModel.objects.all()
    serializer_class = PrintingModelSerializer


class QualityViewSet(viewsets.ModelViewSet):
    queryset = PrintedModelQuality.objects.all()
    serializer_class = PrintingQualitySerializer


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class PrinterGCODEAPI(APIView):

    def get(self, request, **kwargs):
        if not "printer_id" in kwargs or not "command" in kwargs:
            return Response(data={"status":"The printer id or command is missing"}, status=status.HTTP_400_BAD_REQUEST)

        execute_gcode_command(printer_id=kwargs["printer_id"], command=kwargs["command"])

        return Response(data={"printer_id":kwargs["printer_id"], "command":kwargs["command"]},
                        status=status.HTTP_200_OK)


class QueuesListApi(ListAPIView):
    queryset = Queue.objects.all()

    class QueueSerializer(serializers.ModelSerializer):
        printing_models = PrintingModelSerializer(read_only=True, many=True, required=False)
        printing_models_id = serializers.PrimaryKeyRelatedField(
            queryset=PrintingModel.objects.all(), source='printing_models', write_only=True, many=True, required=False
        )

        class Meta:
            model = Queue
            fields = ('printer', 'printing_models', 'printing_models_id')

    def get_serializer(self, *args, **kwargs):
        return self.QueueSerializer()

    def get(self, request, *args, **kwargs):
        queues = get_queues({'parent_lookup_printer': kwargs['printer_id']})
        data = self.QueueSerializer(queues, many=True)
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
            except Exception as e:
                print(type(e))
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

    def patch(self, request, **kwargs):
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

    def patch(self, request, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        if serializer.is_valid():
            queue = get_queue(kwargs['printer_id'])
            remove_models_from_queue(queue, serializer.validated_data)
            return Response(data={"status": "Models have been deleted successfully"})

        return Response(data={"status": "Given model or printer does not exist"}, )
