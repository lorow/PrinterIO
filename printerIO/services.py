from printerIO.models import Queue, Printer
from printerIO.utils import flatten_list
from printerIO.selectors import get_printer
from collections import OrderedDict
from printerIO.utils import validate_build_volume
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


def create_printer(name: str, build_volume: str, printer_type: str, username: str, password: str, thumbnail=None,
                   ip_address=None, port_number: int = None, is_printing: bool = False,) -> Printer:

    if not build_volume or not validate_build_volume(build_volume):
        raise ValidationError(detail="The provided build volume is invalid: {{build_volume}}"
                              .format(build_volume=build_volume))

    password_to_save = make_password(password)

    printer = Printer.objects.create()

    printer.name = name
    printer.build_volume = build_volume
    printer.printer_type = printer_type
    printer.username = username
    printer.password = password_to_save
    printer.thumbnail = thumbnail
    printer.ip_address = ip_address
    printer.port_number = port_number
    printer.is_printing = is_printing

    printer.save()
    return printer


def delete_printer(printer_id: int) -> None:
    printer = get_printer(printer_id)
    printer.delete()


def update_printer(printer_id: int, name: str, build_volume: str, printer_type: str, username: str,
                   password: str, thumbnail=None, ip_address=None,
                   port_number: int = None, is_printing: bool = False) -> Printer:

    printer = get_printer(printer_id)
    new_password = make_password(password)

    printer.name = name
    printer.build_volume = build_volume
    printer.printer_type = printer_type
    printer.username = username
    printer.password = new_password
    printer.thumbnail = thumbnail
    printer.ip_address = ip_address
    printer.port_number = port_number
    printer.is_printing = is_printing

    printer.save()

    return printer


def create_queue(printer: int, printing_models: OrderedDict) -> Queue:
    printer_object = Printer.objects.get(id=printer)
    queue = Queue.objects.create(printer=printer_object)
    queue.printing_models.set(flatten_list(printing_models.values()))
    queue.save()

    return queue


def delete_queue(queue: Queue) -> None:
    queue.delete()


def add_models_to_queue(queue: Queue, models_to_add: dict) -> Queue:
    for model in flatten_list(models_to_add.values()):
        queue.printing_models.add(model.id)

    queue.save()
    return queue


def remove_models_from_queue(queue: Queue, models_to_remove: dict) -> Queue:
    for model in flatten_list(models_to_remove.values()):
        queue.printing_models.remove(model.id)

    queue.save()
    return queue
