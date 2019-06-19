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
                  'is_printing', 'is_paused', 'number_of_extruders',
                  'has_heated_chamber', 'X_Api_Key')


class PrintingQualitySerializer(serializers.ModelSerializer):
    printer = PrinterSerializer()
    model = PrintingModelSerializer()

    class Meta:
        model = PrintedModelQuality
        fields = '__all__'


class FilamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Filament
        fields = ('name', 'producer', 'colour', 'diameter',
                        'weight', 'filament_left', 'filament_type', 'price')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskCategory
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Task
        fields = '__all__'
