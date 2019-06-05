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
from django.conf import settings
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from printerIO.routers import router
from printerIO.views import *


urlpatterns = [
    path('', include_docs_urls(title="PrinterIO API guide")),
    path('api/', include(router.urls)),

    path('api/printers/<int:printer_id>/commands/<str:commands>/', PrinterGCODECommandsAPI.as_view()),
    path('api/printers/<int:printer_id>/move/<str:axis>/<str:amount>/', PrinterMoveAxisAPI.as_view()),

    path('api/printers/<int:printer_id>/queue/', QueuesListApi.as_view()),
    path('api/printers/<int:printer_id>/queue/create/', QueueCreateApi.as_view()),
    path('api/printers/<int:printer_id>/queue/delete/', QueueDeleteApi.as_view()),
    path('api/printers/<int:printer_id>/queue/add/', AddModelsToQueueApi.as_view()),
    path('api/printers/<int:printer_id>/queue/remove/', RemoveModelsFromQueueApi.as_view()),
    path('api/printers/<int:printer_id>/queue/next/', PrinterStartNextJobApi.as_view()),

    path('api/printers/<int:printer_id>/job/<int:file_id>/start/', PrinterJobStartApi.as_view()),
    path('api/printers/<int:printer_id>/job/<int:file_id>/pause/', PrinterJobPauseApi.as_view()),
    path('api/printers/<int:printer_id>/job/<int:file_id>/cancel/', PrinterJobCancelApi.as_view()),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls',  namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        })
    ]
