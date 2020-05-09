from rest_framework import serializers
from printerIO.models import Printer


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = (
            "id",
            "name",
            "thumbnail",
            "build_volume",
            "printer_type",
            "ip_address",
            "port_number",
            "is_printing",
            "is_paused",
            "number_of_extruders",
            "has_heated_chamber",
            "X_Api_Key",
        )


class GCODECommandSerializer(serializers.Serializer):
    commands = serializers.CharField()


class DirectionSerializer(serializers.Serializer):
    axis = serializers.ListField(child=serializers.CharField())
    values = serializers.ListField(child=serializers.IntegerField())


class JobSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()


class PrinterTempSerializer(serializers.Serializer):
    temperatures = serializers.ListField(child=serializers.IntegerField())
    tool_type = serializers.ChoiceField(choices=["bed", "tool", "chamber"])
