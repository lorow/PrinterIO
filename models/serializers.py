from rest_framework import serializers
from printerIO.models import PrintingModel


class PrintingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintingModel
        fields = ("id", "file", "name", "thing_dimensions")
