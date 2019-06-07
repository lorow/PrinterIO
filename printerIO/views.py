from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from printerIO.serializers import *
from printerIO.selectors import *
from printerIO.services import *
from printerIO.models import *


class PrintingModelViewSet(viewsets.ModelViewSet):
    queryset = PrintingModel.objects.all()
    serializer_class = PrintingModelSerializer


class QualityViewSet(viewsets.ModelViewSet):
    queryset = PrintedModelQuality.objects.all()
    serializer_class = PrintingQualitySerializer


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class PrinterGCODECommandsAPI(APIView):

    def get(self, request, **kwargs):
        if "commands" not in kwargs:
            return Response(data={"status": "The command is missing"}, status=status.HTTP_400_BAD_REQUEST)

        if check_if_printer_is_connected(get_printer(kwargs["printer_id"])):
            execute_gcode_commands(**kwargs)

            return Response(data={"printer_id": kwargs["printer_id"], "commands": kwargs["commands"]},
                            status=status.HTTP_200_OK)

        return Response(data={"status": "The selected printer is not connected right not, check the connection"},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)


class PrinterMoveAxisAPI(APIView):
    """Endpoint for moving around tools of the printer, you can provide only one axis with one value
    or multiple as [x,z], [10,20]"""

    def get(self, request, **kwargs):

        if "axis" not in kwargs or "amount" not in kwargs:
            return Response(data={"status": "You must provide both, the direction and amount"},
                            status=status.HTTP_400_BAD_REQUEST)

        if check_if_printer_is_connected(get_printer(kwargs["printer_id"])):
            move_axis_printer(**kwargs)
            return Response(data={**kwargs}, status=status.HTTP_200_OK)

        return Response(data={"status": "The selected printer is not connected, check the connection"},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)


class PrinterJobStartApi(APIView):
    """API endpoint for implicitly creating a one-file long queue, and therefore starting the print job NOTE: The print
    job won't start unless the printer is set as "ready to print" NOTE 2: If there is an existing queue, the file will
    be added to it
    """
    def post(self, request, **kwargs):

        if check_if_printer_is_connected(get_printer(kwargs["printer_id"])):
            printer_data = start_print_job(**kwargs)
            return Response(data={"status": "The job has been started successfully",
                                  "socket_connection_info": {
                                      "ip": printer_data.ip_address,
                                      "port": printer_data.port_number,
                                      "endpoint": "/chuj/to/wie"
                                  }},
                            status=status.HTTP_200_OK)

        return Response(data={"status": "The printer is not connected, check your connection"},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)


class PrinterJobPauseApi(APIView):
    """API endpoint for pausing the printing job. It can also be used to un-pause the job since it keeps the
    state
    """
    def get(self, request, **kwargs):
        try:
            pause_print_job(**kwargs)
            return Response(data={"status": "The job has been successfully paused"}, status=status.HTTP_200_OK)
        except ValidationError as val:
            return Response(data={"status": val.message}, status=status.HTTP_400_BAD_REQUEST)


class PrinterJobCancelApi(APIView):
    """
    API endpoint for canceling the printing job.
    """
    def get(self, request, **kwargs):
        try:
            cancel_print_job(**kwargs)
            return Response(data={"status": ""}, status=status.HTTP_200_OK)
        except ValidationError as val:
            return Response(data={"status": val.message}, status=status.HTTP_400_BAD_REQUEST)


class PrinterStartNextJobApi(APIView):
    """
    API endpoint for letting the PrinterIO system know that it can safely issue next print job
    """

    def get(self, request, **kwargs):
        call_next_job(**kwargs)
        return Response()


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
        try:
            queues = get_queue_by_queue_id(kwargs['printer_id'])
            data = self.QueueSerializer(queues, many=False)
            return Response(data.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"status":"Queue with this ID does not exists"}, status=status.HTTP_400_BAD_REQUEST)


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

        # DOES NOT START PRINTING
        # QUEUE DOES NOT COMMUNICATE WITH PRINTING MANAGER

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
        try:
            queue = get_queue_by_queue_id(kwargs['printer_id'])
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
            queue = get_queue_by_queue_id(kwargs['printer_id'])
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
            queue = get_queue_by_queue_id(kwargs['printer_id'])
            remove_models_from_queue(queue, serializer.validated_data)
            return Response(data={"status": "Models have been deleted successfully"})

        return Response(data={"status": "Given model or printer does not exist"}, )
