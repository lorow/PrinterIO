from rest_framework import routers
from rest_framework_extensions.routers import NestedRouterMixin
from printerIO import views

class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass

router = NestedDefaultRouter()
router.register('models', views.PrintingModelViewSet)
router.register('printers', views.PrinterViewSet)\
    .register('queues', views.TestingQueueViewSet, basename="printer-queue",
              parents_query_lookups=['printer'])
router.register('results', views.QualityViewSet)

