from django.apps import AppConfig
from printers.managers import PrintingManager


class PrinterIOConfig(AppConfig):
    name = 'printerIO'
    printing_manager = PrintingManager()