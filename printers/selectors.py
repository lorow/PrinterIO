from typing import Iterable
from printerIO.models import Printer


def get_printers() -> Iterable[Printer]:
    return Printer.objects.all()


def get_printer(printer_id: int) -> Printer:
    return Printer.objects.get(id=printer_id)
