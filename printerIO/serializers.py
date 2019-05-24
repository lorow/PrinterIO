from rest_framework import serializers
from printerIO.models import *


class PrintingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintingModel
        fields = ('id', 'file', 'name', 'thing_dimensions')


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ('id', 'name', 'thumbnail', 'build_volume',
                  'printer_type', 'ip_address', 'port_number',
                  'is_printing')


class QueueSerializer(serializers.ModelSerializer):
    printing_models = PrintingModelSerializer(read_only=True,many=True, required=False)
    printing_models_id = serializers.PrimaryKeyRelatedField(
        queryset=PrintingModel.objects.all(), source='printing_models', write_only=True, many=True, required=False
    )

    class Meta:
        model = Queue
        fields = ('printer', 'printing_models', 'printing_models_id')


class PrintingQualitySerializer(serializers.ModelSerializer):
    printer = PrinterSerializer()
    model = PrintingModelSerializer()

    class Meta:
        model = PrintedModelQuality
        fields = '__all__'
