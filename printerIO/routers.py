from rest_framework_nested import routers
from printerIO import views as printerIOViews
from queues import views as queueViews
from models.views import *
from printers.views import PrinterViewSet


router = routers.DefaultRouter(trailing_slash="")
router.register("models", PrintingModelViewSet)
router.register("printers", PrinterViewSet)
router.register("results", printerIOViews.QualityViewSet)
router.register("filaments", printerIOViews.FilamentViewSet)
router.register("categories", printerIOViews.CategoryViewSet)
router.register("tasks", printerIOViews.TaskViewSet)
router.register("problems", printerIOViews.ProblemViewSet)

queue_router = routers.NestedDefaultRouter(router, r"printers", lookup="printers")
queue_router.register("queue", queueViews.QueueViewset)
