from rest_framework import routers
from printerIO import views

router = routers.DefaultRouter()

router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)