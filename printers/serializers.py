from rest_framework import serializers
from printerIO.models import Printer


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ('id', 'name', 'thumbnail', 'build_volume',
                  'printer_type', 'ip_address', 'port_number',
                  'is_printing', 'is_paused', 'number_of_extruders',
                  'has_heated_chamber', 'X_Api_Key')
