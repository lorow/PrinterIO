from rest_framework.response import Response
from .serializers import PrinterSerializer
from .services import *
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from printerIO.models import Printer
from rest_framework import viewsets
import django_filters


# Create your views here.
class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = (
        'name', 'build_volume', 'printer_type', 'is_printing',
        'is_paused', 'number_of_extruders', 'has_heated_chamber'
    )


class PrinterGCODECommandsAPI(APIView):

    def post(self, request, **kwargs):
        if "commands" not in kwargs:
            return Response(
                data={"status": "The command is missing"},
                status=status.HTTP_400_BAD_REQUEST
            )

        execute_gcode_commands(**kwargs)

        return Response(
            data={
                "printer_id": kwargs["printer_id"],
                "commands": kwargs["commands"]
            },
            status=status.HTTP_200_OK
        )


class PrinterMoveAxisAPI(APIView):
    """
    Endpoint for moving around tools of the printer,
    you can provide only one axis with one value
    or multiple as [x,z], [10,20]
    """

    class DirectionSerializer(serializers.Serializer):
        axis = serializers.ListField(child=serializers.CharField())
        values = serializers.ListField(child=serializers.IntegerField())

    def get_serializer(self):
        return self.DirectionSerializer()

    def post(self, request, **kwargs):

        serializer = self.DirectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        move_axis_printer(
            **serializer.validated_data,
            printer_id=kwargs["printer_id"]
        )

        return Response(
            data={**kwargs},
            status=status.HTTP_200_OK
        )


class PrinterJobStartApi(APIView):
    """
    API endpoint for implicitly creating a one-file long queue,
    and therefore starting the print job
    # TODO this should send an exception if not ready to print
    NOTE: The print job won't start unless
    the printer is set as "ready to print"
    NOTE 2: If there is an existing queue, the file will be added to it
    """

    def post(self, request, **kwargs):

        printer_data = start_print_job(**kwargs)
        return Response(
            data={
                "status": "The job has been started successfully",
                "socket_connection_info": {
                    "ip": printer_data.ip_address,
                    "port": printer_data.port_number,
                    "endpoint": "/to/be/updated"
                }},
            status=status.HTTP_200_OK
        )


class PrinterJobPauseApi(APIView):
    """
    API endpoint for pausing the printing job.
    It can also be used to un-pause the job since it keeps the state
    """

    def post(self, request, **kwargs):
        pause_print_job(**kwargs)
        return Response(
            data={"status": "The job has been successfully paused"},
            status=status.HTTP_200_OK
        )


class PrinterJobCancelApi(APIView):
    """
    API endpoint for canceling the printing job.
    """

    def post(self, request, **kwargs):

        cancel_print_job(**kwargs)
        return Response(
            data={"status": "The job has been canceled successfully"},
            status=status.HTTP_200_OK
        )


class PrinterStartNextJobApi(APIView):
    """
    API endpoint for letting the PrinterIO system know
    that it can safely issue next print job

    NOTE: this should be called by the frontend only when the user
    has been prompted that it is in fact safe to proceed
    """

    def post(self, request, **kwargs):
        call_next_job(**kwargs)
        return Response(
            data={"status": "Started next job successfully"},
            status=status.HTTP_200_OK
        )


class PrinterSetBedTemperatureApi(APIView):

    class BedTempSerializer(serializers.Serializer):
        temperature = serializers.IntegerField()

    def get_serializer(self):
        return self.BedTempSerializer()

    def post(self, request, **kwargs):
        data = self.BedTempSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        set_printer_bed_temperature(
            printer_id=kwargs["printer_id"],
            temperature=data.validated_data["temperature"]
        )

        return Response(
            data={
                "status": """
                The temperature for the Bed has been successfully set to {temp}
                """.format(
                    temp=data.validated_data["temperature"]
                )
            },
            status=status.HTTP_200_OK
        )


class PrinterSetToolTemperature(APIView):

    class InputSerializer(serializers.Serializer):
        temperatures = serializers.ListField(child=serializers.IntegerField())

    def get_serializer(self):
        return self.InputSerializer()

    def post(self, request, **kwargs):

        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        set_printer_tool_temperature(
            kwargs["printer_id"], data.validated_data["temperatures"]
        )

        return Response(
            data={
                "status": """
                    The temperatures for the tools have been set successfully
                """
            },
            status=status.HTTP_200_OK)


class PrinterSetChamberTemperature(APIView):

    class ChamberTemperatureSerializer(serializers.Serializer):
        temperature = serializers.IntegerField()

    def get_serializer(self):
        return self.ChamberTemperatureSerializer()

    def post(self, request, **kwargs):
        data = self.ChamberTemperatureSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        set_printer_chamber_temperature(
            kwargs["printer_id"], data.validated_data["temperature"])

        return Response(
            data={
                "status": """
                    The temperature for the chamber has been set successfully
                """
            },
            status=status.HTTP_200_OK)
