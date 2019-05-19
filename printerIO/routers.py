from rest_framework import routers
from printerIO import views

router = routers.DefaultRouter()
router.register('model', views.PrintingModelViewSet)
router.register('printer', views.PrinterViewSet)
router.register('quality', views.QualityViewSet)