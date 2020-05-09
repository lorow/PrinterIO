from rest_framework import serializers
from printerIO.models import *
from printers.serializers import PrinterSerializer
from models.serializers import PrintingModelSerializer

# stats app


class PrintingQualitySerializer(serializers.ModelSerializer):
    printer = PrinterSerializer()
    model = PrintingModelSerializer()

    class Meta:
        model = PrintedModelQuality
        fields = "__all__"


class FilamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filament
        fields = (
            "name",
            "producer",
            "colour",
            "diameter",
            "weight",
            "filament_left",
            "filament_type",
            "price",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Task
        fields = "__all__"


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = "__all__"
