from printerIO.models import Queue, Printer
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import QueueSerializer
import django_filters


class QueueViewset(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ("printer",)

    def create(self, request, **kwargs):
        serializer = QueueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data["printer"] = get_object_or_404(Printer, pk=kwargs["printers_pk"])

        printing_models = data.pop("printing_models")
        queue = Queue.objects.create(**data)
        queue.printing_models.set(printing_models)
        queue.save()

        return Response(data)

    # TODO override update too
