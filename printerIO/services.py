from printerIO.models import Queue, Printer
from printerIO.utils import flatten_list, issue_command_to_printer
from printerIO.selectors import get_printer
from collections import OrderedDict


def execute_gcode_commands(printer_id: int, commands: str) -> None:
    printer = get_printer(printer_id)
    command_endpoint = "/api/printer/command"

    if printer.X_Api_Key == "":
        raise ValueError

    issue_command_to_printer(printer_ip=printer.ip_address,
                             printer_port=printer.port_number,
                             endpoint=command_endpoint,
                             api_key=printer.X_Api_Key,
                             json={"commands": commands.split(',')})


def move_axis_printer(printer_id: int, axis, amount) -> None:
    printer = get_printer(printer_id)
    command_endpoint = "/api/printer/printhead"

    demanded_directions = axis.split(',')
    provided_amounts = [int(value) for value in amount.split(",")]

    if not len(demanded_directions) == len(provided_amounts):
        raise ValueError # TODO

    json = dict(zip(demanded_directions, provided_amounts))
    json["command"] = "jog"

    req=issue_command_to_printer(printer_ip=printer.ip_address,
                             printer_port=printer.port_number,
                             endpoint=command_endpoint,
                             api_key=printer.X_Api_Key,
                             json=json)

    print(req)


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
