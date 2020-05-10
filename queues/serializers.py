from rest_framework import serializers
from printerIO.models import PrintingModel, Queue
from printers.serializers import PrinterSerializer
from models.serializers import PrintingModelSerializer


class QueueSerializer(serializers.ModelSerializer):

    printer_info = PrinterSerializer(source="printer", read_only=True)

    printing_models_info = PrintingModelSerializer(
        source="printing_models", many=True, read_only=True
    )
    printing_models = serializers.PrimaryKeyRelatedField(
        queryset=PrintingModel.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Queue
        fields = ("printer_info", "printing_models_info", "printing_models")
