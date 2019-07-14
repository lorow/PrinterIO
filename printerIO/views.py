from rest_framework import viewsets
from printerIO.serializers import *
from printerIO.models import *
import django_filters


class QualityViewSet(viewsets.ModelViewSet):
    queryset = PrintedModelQuality.objects.all()
    serializer_class = PrintingQualitySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('printer', 'model', 'quality_number', 'was_cancelled')


class FilamentViewSet(viewsets.ModelViewSet):
    queryset = Filament.objects.all()
    serializer_class = FilamentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('name', 'producer', 'colour', 'diameter',
                        'weight', 'filament_left', 'filament_type', 'price')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = TaskCategory.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('name',)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('title', 'created', 'due', 'category')


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('severity', 'title', 'description', 'timestamp', 'state')
