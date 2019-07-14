from .serializers import PrintingModelSerializer
from printerIO.models import PrintingModel
from rest_framework import viewsets
import django_filters


class PrintingModelViewSet(viewsets.ModelViewSet):
    queryset = PrintingModel.objects.all()
    serializer_class = PrintingModelSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('name', 'thing_dimensions')

