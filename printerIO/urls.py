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

    path('api/printers/<int:printer_id>/command/<str:command>/', PrinterGCODEAPI.as_view()),

    path('api/printers/<int:printer_id>/queue/', QueuesListApi.as_view()),
    path('api/printers/<int:printer_id>/create_queue/', QueueCreateApi.as_view()),
    path('api/printers/<int:printer_id>/remove_queue/', QueueDeleteApi.as_view()),
    path('api/printers/<int:printer_id>/queue/add_models/', AddModelsToQueueApi.as_view()),
    path('api/printers/<int:printer_id>/queue/remove_models/', RemoveModelsFromQueueApi.as_view()),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls',  namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        })
    ]
