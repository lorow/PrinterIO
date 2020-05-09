from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    PrinterSerializer,
    GCODECommandSerializer,
    DirectionSerializer,
    JobSerializer,
    PrinterTempSerializer,
)
from .services import *
from rest_framework.views import APIView
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from printerIO.models import Printer
import django_filters


# Create your views here.
class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = (
        "name",
        "build_volume",
        "printer_type",
        "is_printing",
        "is_paused",
        "number_of_extruders",
        "has_heated_chamber",
    )

    @swagger_auto_schema(request_body=GCODECommandSerializer)
    @action(detail=True, methods=["post"])
    def gcode_command(self, request, pk=None):
        """
        Endpoint that accepts the ID of the printer and list of commands
        NOTE: The commands aren't escaped, so be wary when using this endpoint
        """

        serializer = GCODECommandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        execute_gcode_commands(printer_id=pk, **serializer.validated_data)
        return Response(
            data={"printer_id": kwargs["printer_id"], "commands": kwargs["commands"]},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(request_body=DirectionSerializer)
    @action(detail=True, methods=["post"])
    def move_axis(self, request, pk=None):
        """
        Endpoint for moving around the tools of the printer,
        you can provide only one axis with one value
        or multiple as [x,z], [10,20]
        """

        serializer = DirectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        move_axis_printer(**serializer.validated_data, printer_id=kwargs["printer_id"])
        return Response(data={**kwargs}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=JobSerializer)
    @action(detail=True, methods=["post"])
    def start_job(self, request, pk=None):
        """
        API endpoint for implicitly creating a one-file long queue,
        and therefore starting the print job
        # TODO this should send an exception if not ready to print
        NOTE: The print job won't start unless
        the printer is set as "ready to print"
        NOTE 2: If there is an existing queue, the file will be added to it
        """
        serializer = JobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        printer_data = start_print_job(printer_id=pk, **serializer.validated_data)
        return Response(
            data={
                "status": "The job has been started successfully",
                "socket_connection_info": {
                    "ip": printer_data.ip_address,
                    "port": printer_data.port_number,
                    "endpoint": "/to/be/updated",
                },
            },
            status=status.HTTP_200_OK,
        )

    # I'm passing an empty serializers so that the docs don't confuse people
    # Passing an empty serializer instance makes yasg generate an
    # empty data body, required with POST request
    @swagger_auto_schema(request_body=serializers.Serializer())
    @action(detail=True, methods=["post"])
    def pause_current_job(self, request, pk=None):
        """
        API endpoint for pausing the current printing job.
        It can also be used to un-pause the job since it keeps the state
        """
        pause_print_job(printer_id=pk)
        return Response(
            data={"status": "The job has been successfully paused"},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(request_body=serializers.Serializer())
    @action(detail=True, methods=["post"])
    def cancel_print_job(self, request, pk=None):
        """
        API endpoint for canceling the printing job.
        """
        cancel_print_job(**kwargs)
        return Response(
            data={"status": "The job has been canceled successfully"},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(request_body=PrinterTempSerializer)
    @action(detail=True, methods=["post"])
    def set_temperature(self, request, pk=None):
        """
        Endpoint for setting the temperature of either:
        tool, bed or the chamber
        """
        data = self.PrinterTempSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        set_printer_temperature(printer_id=kwargs["printer_id"], **data.validated_data)

        return Response(
            data={
                "status": """
                The temperature for the Bed has been successfully set to {temp}
                """.format(
                    temp=data.validated_data["temperature"]
                )
            },
            status=status.HTTP_200_OK,
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
            data={"status": "Started next job successfully"}, status=status.HTTP_200_OK
        )
