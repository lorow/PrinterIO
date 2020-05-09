from rest_framework import routers
from rest_framework_extensions.routers import NestedRouterMixin
from printerIO import views

from models.views import *
from printers.views import PrinterViewSet


class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = ""


router = NestedDefaultRouter()
router.register("models", PrintingModelViewSet)
router.register("printers", PrinterViewSet)
router.register("results", views.QualityViewSet)
router.register("filaments", views.FilamentViewSet)
router.register("categories", views.CategoryViewSet)
router.register("tasks", views.TaskViewSet)
router.register("problems", views.ProblemViewSet)
