from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from printerIO.serializers import *
from printerIO.selectors import *
from printerIO.services import *
from printerIO.models import *
import django_filters


class PrintingModelViewSet(viewsets.ModelViewSet):
    queryset = PrintingModel.objects.all()
    serializer_class = PrintingModelSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('name', 'thing_dimensions')

class QualityViewSet(viewsets.ModelViewSet):
    queryset = PrintedModelQuality.objects.all()
    serializer_class = PrintingQualitySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('printer', 'model', 'quality_number', 'was_cancelled')


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('name', 'build_volume', 'printer_type', 'is_printing',
                        'is_paused', 'number_of_extruders', 'has_heated_chamber')


class FilamentViewSet(viewsets.ModelViewSet):
    queryset = Filament.objects.all()
    serializer_class = FilamentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('name', 'producer', 'colour', 'diameter',
                        'weight', 'filament_left', 'filament_type', 'price')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = TaskCategory.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('name',)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('title', 'created', 'due', 'category')


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('severity', 'title', 'description', 'timestamp', 'state')


class PrinterGCODECommandsAPI(APIView):

    def get(self, request, **kwargs):
        if "commands" not in kwargs:
            return Response(data={"status": "The command is missing"}, status=status.HTTP_400_BAD_REQUEST)

        execute_gcode_commands(**kwargs)

        return Response(data={"printer_id": kwargs["printer_id"], "commands": kwargs["commands"]},
                        status=status.HTTP_200_OK)


class PrinterMoveAxisAPI(APIView):
    """Endpoint for moving around tools of the printer, you can provide only one axis with one value
    or multiple as [x,z], [10,20]"""

    class InputSerializer(serializers.Serializer):
        axis = serializers.ListField(child=serializers.CharField())
        values = serializers.ListField(child=serializers.IntegerField())

    def get_serializer(self):
        return self.InputSerializer()

    def post(self, request, **kwargs):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        move_axis_printer(**serializer.validated_data, printer_id=kwargs["printer_id"])

        return Response(data={**kwargs}, status=status.HTTP_200_OK)


class PrinterJobStartApi(APIView):
    """API endpoint for implicitly creating a one-file long queue, and therefore starting the print job NOTE: The print
    job won't start unless the printer is set as "ready to print" NOTE 2: If there is an existing queue, the file will
    be added to it
    """
    def post(self, request, **kwargs):

        printer_data = start_print_job(**kwargs)
        return Response(data={"status": "The job has been started successfully",
                              "socket_connection_info": {
                                  "ip": printer_data.ip_address,
                                  "port": printer_data.port_number,
                                  "endpoint": "/chuj/to/wie"
                              }},
                        status=status.HTTP_200_OK)


class PrinterJobPauseApi(APIView):
    """API endpoint for pausing the printing job. It can also be used to un-pause the job since it keeps the
    state
    """
    def get(self, request, **kwargs):
        pause_print_job(**kwargs)
        return Response(data={"status": "The job has been successfully paused"}, status=status.HTTP_200_OK)


class PrinterJobCancelApi(APIView):
    """
    API endpoint for canceling the printing job.
    """
    def get(self, request, **kwargs):

        cancel_print_job(**kwargs)
        return Response(data={"status": ""}, status=status.HTTP_200_OK)


class PrinterStartNextJobApi(APIView):
    """
    API endpoint for letting the PrinterIO system know that it can safely issue next print job
    """

    def get(self, request, **kwargs):
        call_next_job(**kwargs)
        return Response()


class PrinterSetBedTemperatureApi(APIView):

    class InputSerializer(serializers.Serializer):
        temperature = serializers.IntegerField()

    def get_serializer(self):
        return self.InputSerializer()

    def post(self, request, **kwargs):
        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        set_printer_bed_temperature(
            printer_id=kwargs["printer_id"],
            temperature=data.validated_data["temperature"]
        )

        return Response(data={"status": "The temperature for the {tool} has been successfully set to {temp}"
                        .format(tool=data.validated_data["tool_type"],
                                temp=data.validated_data["temperature"])},

                        status=status.HTTP_200_OK)


class PrinterSetToolTemperature(APIView):

    class InputSerializer(serializers.Serializer):
        temperatures = serializers.ListField(child=serializers.IntegerField())

    def get_serializer(self):
        return self.InputSerializer()

    def post(self, request, **kwargs):

        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        set_printer_tool_temperature(kwargs["printer_id"], data.validated_data["temperatures"])

        return Response(data={"status": "The temperatures for the tools have been set successfully"},
                        status=status.HTTP_200_OK)


class PrinterSetChamberTemperature(APIView):

    class InputSerializer(serializers.Serializer):
        temperature = serializers.IntegerField()

    def get_serializer(self):
        return self.InputSerializer()

    def post(self, request, **kwargs):
        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        set_printer_chamber_temperature(kwargs["printer_id"], data.validated_data["temperature"])

        return Response(data={"status": "The temperature for the chamber has been set successfully"},
                        status=status.HTTP_200_OK)


class QueuesListApi(RetrieveAPIView):
    """API endpoint for listing all the currently running printing queues"""
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
        queues = get_queue_by_printer_id(kwargs['printer_id'])
        data = self.QueueSerializer(queues, many=False)
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
        serializer.is_valid(raise_exception=True)
        create_queue(kwargs['printer_id'], serializer.validated_data)
        return Response(data={"status": "created successfully"},
                        status=status.HTTP_202_ACCEPTED)


class QueueDeleteApi(DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        queue = get_queue_by_queue_id(kwargs['printer_id'])
        delete_queue(queue)
        return Response(data={"status": "The queue has been successfully deleted"},
                        status=status.HTTP_200_OK)


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

        serializer.is_valid(raise_exception=True)
        queue = get_queue_by_queue_id(kwargs['printer_id'])
        add_models_to_queue(queue, serializer.validated_data)
        return Response(data={"status": "The models have been added successfully"}, status=status.HTTP_200_OK)


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
        serializer.is_valid(raise_exception=True)

        queue = get_queue_by_queue_id(kwargs['printer_id'])
        remove_models_from_queue(queue, serializer.validated_data)
        return Response(data={"status": "Models have been deleted successfully"})
