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


# class PrinterViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
#     queryset = Printer.objects.all()
#     serializer_class = PrinterSerializer

class QualityViewSet(viewsets.ModelViewSet):
    queryset = PrintedModelQuality.objects.all()
    serializer_class = PrintingQualitySerializer


class PrinterListApi(ListAPIView):

    def get_serializer(self, *args, **kwargs):
        return PrinterSerializer()

    def get(self, request, *args, **kwargs):
        printers = get_printers()
        data = PrinterSerializer(printers, many=True)
        return Response(data.data, status=status.HTTP_200_OK)


class PrinterDetailAPi(ListAPIView):

    def get_serializer(self, *args, **kwargs):
        return PrinterSerializer()

    def get(self, request, *args, **kwargs):
        try:
            printer = get_printer(kwargs['printer_id'])
            data = PrinterSerializer(printer)
            return Response(data.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"status": "this printer does not exists"}, status=status.HTTP_404_NOT_FOUND)


class PrinterCreateAPi(CreateAPIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(help_text="The name of your printer")
        build_volume = serializers.CharField(help_text="The usable build volume of you printer, provided as XxYxZ, "
                                                       "for example 300x300x300")
        printer_type = serializers.ChoiceField(["CR", "DL"], help_text="Type of your printer, CR - Cartesian, "
                                                                       "DL - Delta")
        username = serializers.CharField(help_text="Login to the octoprint instance")
        password = serializers.CharField(style={'input_type': 'password'}, help_text="Your password to the octoprint account"
                                                                                     "don't worry, it's stored securely")
        thumbnail = serializers.ImageField(required=False, style={'input_type': 'file'}, help_text="The thumbnail you "
                                                                                                   "want this printer"
                                                                                                   "to be identified with")
        ip_address = serializers.IPAddressField(default="0.0.0.0", required=False, help_text="IP address of the raspberry pi"
                                                                                             "running your octoprint instace")
        port_number = serializers.IntegerField(default=5000, required=False, help_text="The port it's running at")
        is_printing = serializers.BooleanField(default=False, required=False)

    def get_serializer(self, *args, **kwargs):
        return self.InputSerializer()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_printer(**serializer.validated_data)
        return Response()


class PrinterDeleteAPi(DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        delete_printer(kwargs["printer_id"])
        return Response({"status":"deleted successfully"}, status=status.HTTP_200_OK)


class PrinterUpdateAPi(UpdateAPIView):
    class InputSerializer(serializers.Serializer):
        # Possible DRY volition
        name = serializers.CharField(help_text="The name of your printer")
        build_volume = serializers.CharField(help_text="The usable build volume of you printer, provided as XxYxZ, "
                                                       "for example 300x300x300")
        printer_type = serializers.ChoiceField(["CR", "DL"], help_text="Type of your printer, CR - Cartesian, "
                                                                       "DL - Delta")
        username = serializers.CharField(help_text="Login to the octoprint instance")
        password = serializers.CharField(style={'input_type': 'password'}, help_text="Your password to the octoprint account"
                                                                                     "don't worry, it's stored securely")
        thumbnail = serializers.ImageField(required=False, style={'input_type': 'file'}, help_text="The thumbnail you "
                                                                                                   "want this printer"
                                                                                                   "to be identified with")
        ip_address = serializers.IPAddressField(default="0.0.0.0", required=False, help_text="IP address of the raspberry pi"
                                                                                             "running your octoprint instace")
        port_number = serializers.IntegerField(default=5000, required=False, help_text="The port it's running at")
        is_printing = serializers.BooleanField(default=False, required=False)

    def get_serializer(self, *args, **kwargs):
        return self.InputSerializer()

    def patch(self, request, *args, **kwargs):
        return Response()

    def update(self, request, *args, **kwargs):
        return Response()


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
