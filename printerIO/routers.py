from rest_framework import routers
from rest_framework_extensions.routers import NestedRouterMixin
from printerIO import views


class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass


router = NestedDefaultRouter()
router.register('models', views.PrintingModelViewSet)
router.register('printers', views.PrinterViewSet)
router.register('results', views.QualityViewSet)
router.register('filaments', views.FilamentViewSet)
router.register('categories', views.CategoryViewSet)
router.register('tasks', views.TaskViewSet)