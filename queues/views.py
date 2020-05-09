from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView
from printerIO.models import Queue, PrintingModel
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from models.serializers import PrintingModelSerializer
from .services import *
from .selectors import *


class QueuesListApi(RetrieveAPIView):
    """API endpoint for listing all the currently running printing queues"""

    queryset = Queue.objects.all()

    class QueueSerializer(serializers.ModelSerializer):
        printing_models = PrintingModelSerializer(
            read_only=True, many=True, required=False
        )
        printing_models_id = serializers.PrimaryKeyRelatedField(
            queryset=PrintingModel.objects.all(),
            source="printing_models",
            write_only=True,
            many=True,
            required=False,
        )

        class Meta:
            model = Queue
            fields = ("printer", "printing_models", "printing_models_id")

    def get_serializer(self, *args, **kwargs):
        return self.QueueSerializer()

    def get(self, request, *args, **kwargs):
        queues = get_queue_by_printer_id(kwargs["printer_id"])
        data = self.QueueSerializer(queues, many=False)
        return Response(data.data, status=status.HTTP_200_OK)


class QueueCreateApi(CreateAPIView):
    class CreateQueueSerializer(serializers.Serializer):
        printing_models_ids = serializers.PrimaryKeyRelatedField(
            source="printing_models",
            write_only=True,
            many=True,
            queryset=PrintingModel.objects.all(),
            help_text="Ids of models you want to add to the queue",
        )

    def get_serializer(self):
        return self.CreateQueueSerializer()

    def post(self, request, *args, **kwargs):

        serializer = self.CreateQueueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_queue(kwargs["printer_id"], serializer.validated_data)
        return Response(
            data={"status": "created successfully"}, status=status.HTTP_202_ACCEPTED
        )


class QueueDeleteApi(DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        queue = get_queue_by_queue_id(kwargs["printer_id"])
        delete_queue(queue)
        return Response(
            data={"status": "The queue has been successfully deleted"},
            status=status.HTTP_200_OK,
        )


class AddModelsToQueueApi(APIView):
    """
    Lets you add one or more models to the existing queue,
    which is identified by the supplied printer_id
    """

    class AddModelsSerializer(serializers.Serializer):
        printing_model_ids = serializers.PrimaryKeyRelatedField(
            source="printing_models",
            write_only=True,
            many=True,
            queryset=PrintingModel.objects.all(),
            help_text="Id of an existing model you want to add to queue",
        )

    def get_serializer(self):
        return self.AddModelsSerializer()

    def patch(self, request, **kwargs):
        serializer = self.AddModelsSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        queue = get_queue_by_queue_id(kwargs["printer_id"])
        add_models_to_queue(queue, serializer.validated_data)
        return Response(
            data={"status": "The models have been added successfully"},
            status=status.HTTP_200_OK,
        )


class RemoveModelsFromQueueApi(APIView):
    """
    Lets you remove one or more models from the existing queue,
    which is identified by the supplied printer_id
    """

    class RemoveModelsSerializer(serializers.Serializer):
        printing_model_ids = serializers.PrimaryKeyRelatedField(
            source="printing_models",
            write_only=True,
            many=True,
            queryset=PrintingModel.objects.all(),
            help_text="Id of an existing model you want to add to queue",
        )

    def get_serializer(self):
        return self.RemoveModelsSerializer()

    def patch(self, request, **kwargs):

        serializer = self.RemoveModelsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        queue = get_queue_by_queue_id(kwargs["printer_id"])
        remove_models_from_queue(queue, serializer.validated_data)
        return Response(data={"status": "Models have been deleted successfully"})
