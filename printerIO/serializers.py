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
    class Meta:
        model = Queue
        fields = ("__all__")
