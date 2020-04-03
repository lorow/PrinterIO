"""printerIO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from django.conf import settings
from django.views.static import serve
# from rest_framework.documentation import include_docs_urls
from printerIO.routers import router
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from printers.views import *
from queues.views import *


schema_view = get_schema_view(
    openapi.Info(
        title="PrinterIO API",
        default_version='v1',
        description="",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui(
        'swagger',
        cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include(router.urls)),

    path('api/printers/<int:printer_id>/commands/<str:commands>',
         PrinterGCODECommandsAPI.as_view()),
    path('api/printers/<int:printer_id>/move', PrinterMoveAxisAPI.as_view()),

    path('api/printers/<int:printer_id>/queue', QueuesListApi.as_view()),
    path('api/printers/<int:printer_id>/queue/create', QueueCreateApi.as_view()),
    path('api/printers/<int:printer_id>/queue/delete', QueueDeleteApi.as_view()),
    path('api/printers/<int:printer_id>/queue/models/add',
         AddModelsToQueueApi.as_view()),
    path('api/printers/<int:printer_id>/queue/models/remove',
         RemoveModelsFromQueueApi.as_view()),
    path('api/printers/<int:printer_id>/queue/next-job',
         PrinterStartNextJobApi.as_view()),

    path('api/printers/<int:printer_id>/job/<int:file_id>/start',
         PrinterJobStartApi.as_view()),
    path('api/printers/<int:printer_id>/job/pause', PrinterJobPauseApi.as_view()),
    path('api/printers/<int:printer_id>/job/cancel',
         PrinterJobCancelApi.as_view()),

    path('api/printers/<int:printer_id>/temperature/bed',
         PrinterSetBedTemperatureApi.as_view()),
    path('api/printers/<int:printer_id>/temperature/tool',
         PrinterSetToolTemperature.as_view()),
    path('api/printers/<int:printer_id>/temperature/chamber',
         PrinterSetChamberTemperature.as_view()),

    path('admin/', admin.site.urls),
    path('auth/', include("djoser.urls")),
    path('auth/', include("djoser.urls.jwt")),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        })
    ]
