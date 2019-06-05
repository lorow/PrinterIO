from django.apps import AppConfig
from printerIO.managers import PrintingManager


class PrinterIOConfig(AppConfig):
    name = 'printerIO'
    printing_manager = PrintingManager()