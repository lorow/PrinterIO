from printerIO.selectors import get_printer, get_queue_by_printer_id, get_model
from printerIO.utils import flatten_list, issue_command_to_printer
from rest_framework.exceptions import ValidationError
from requests.exceptions import ConnectionError
from printerIO.models import Queue, Printer
from printerIO.apps import PrinterIOConfig
from collections import OrderedDict
from printerIO.exceptions import *
import requests


def start_print_job(printer_id: int, file_id: int) -> Printer:
    """Service for implicitly creating a one-file-long queue and letting the octoprint start the job"""

    models = OrderedDict()
    models["printing_models"] = [get_model(file_id)]

    if not check_if_printer_is_connected(get_printer(printer_id)):
        raise ServiceUnavailable("The printer is not connected, check your connection")

    # try grabbing the queue by given printer, if it passes then simply add a model to it and notify the manager
    # if it fails, then create it and start printing
    try:
        queue = get_queue_by_printer_id(printer_id=printer_id)
        new_queue = add_models_to_queue(queue, models)

        PrinterIOConfig.printing_manager.refresh_queue(new_queue, queue.printer)

    except ValidationError:
        queue = create_queue(printer_id, models)

        PrinterIOConfig.printing_manager.get_new_queue(queue, queue.printer)

    printer_to_return = queue.printer
    return printer_to_return


def cancel_print_job(printer_id: int) -> None:
    """Service for canceling the currently running job"""
    printer = get_printer(printer_id)
    cancel_endpoint = "/api/job"

    if printer.is_printing:
        issue_command_to_printer(
            printer_ip=printer.ip_address,
            printer_port=printer.port_number,
            endpoint=cancel_endpoint,
            api_key=printer.X_Api_Key,
            json={"command": "cancel"}
        )

        # since we've canceled it, it's a good idea to update the printer
        printer.is_printing = False
        printer.is_paused = False
        printer.save()

    else:
        raise ValidationError("Cannot cancel since the printer isn't printing")


def pause_print_job(printer_id: int) -> None:
    """service for pausing or resuming the print job"""
    printer = get_printer(printer_id)

    if printer.is_printing:
        pause_endpoint = "/api/job"

        issue_command_to_printer(
            printer_ip=printer.ip_address,
            printer_port=printer.port_number,
            endpoint=pause_endpoint,
            api_key=printer.X_Api_Key,
            json={
                "command": "pause",
                "action": "pause" if printer.is_paused else "resume"
            }
        )

        is_currently_printing = printer.is_paused
        printer.is_paused = not is_currently_printing
        printer.save()
    else:
        raise ValidationError("Cannot pause since the printer isn't currently printing")


def call_next_job(printer_id: int) -> None:
    """An utility service, creating for letting printing manager know that it should issue next job more easily
    This should always be called, even if there is no more work to do, it will close everything automatically"""
    PrinterIOConfig.printing_manager.next_job(get_printer(printer_id))


def execute_gcode_commands(printer_id: int, commands: str) -> None:
    """Service for making the printer execute GCODE commands"""
    printer = get_printer(printer_id)

    if not check_if_printer_is_connected(printer):
        raise ServiceUnavailable("The printer is not connected, check connection")

    command_endpoint = "/api/printer/command"

    issue_command_to_printer(printer_ip=printer.ip_address,
                             printer_port=printer.port_number,
                             endpoint=command_endpoint,
                             api_key=printer.X_Api_Key,
                             json={"commands": commands.split(',')})


def move_axis_printer(printer_id: int = None, axis: str = None, values=None) -> None:
    """Service for issuing the printer to move one or more tools for given amount"""

    printer = get_printer(printer_id)

    if axis is None or values is None:
        raise ValidationError("You must provide both, the amount and the axis")

    if not check_if_printer_is_connected(printer):
        raise ServiceUnavailable("The printer is not connected, check connection")

    command_endpoint = "/api/printer/printhead"

    demanded_directions = axis.split(',')
    provided_amounts = [int(value) for value in values.split(",")]

    if not len(demanded_directions) == len(provided_amounts):
        raise ValidationError("You must provide an equal amount of values for given amount of directions")

    payload = dict(zip(demanded_directions, provided_amounts))
    payload["command"] = "jog"

    issue_command_to_printer(printer_ip=printer.ip_address,
                             printer_port=printer.port_number,
                             endpoint=command_endpoint,
                             api_key=printer.X_Api_Key,
                             json=payload)


def set_printer_bed_temperature(printer_id: int, temperature: int) -> Printer:

    printer = get_printer(printer_id)

    if not check_if_printer_is_connected(printer):
        raise ServiceUnavailable("The printer is not connected, check your connection")

    temperature_endpoint = "/api/printer/bed"
    payload = {
        "command": "target",
        "target": temperature
    }

    req = issue_command_to_printer(
        printer_ip=printer.ip_address,
        printer_port=printer.port_number,
        endpoint=temperature_endpoint,
        api_key=printer.X_Api_Key,
        json=payload
    )

    if req.status_code == 409:
        raise ValidationError("The printer is not operational")

    return printer


def set_printer_tool_temperature(printer_id: int, temperatures: list) -> Printer:

    printer = get_printer(printer_id)
    if not check_if_printer_is_connected(printer):
        raise ServiceUnavailable("The printer is not connected, check your connection")

    if len(temperatures) > printer.number_of_extruders:
        raise ValidationError("Too many temperature values provided, this printer only supports {ext} extrudes"
                              .format(ext=printer.number_of_extruders))

    tool_temperature_endpoint = "/api/printer/tool"

    payload = dict()
    payload["command"] = "target"
    payload["targets"] = {}

    for temperature_id in range(len(temperatures)):
        payload["targets"]["tool{tool_id}".format(tool_id=temperature_id)] = temperatures[temperature_id]

    req = issue_command_to_printer(
        printer_ip=printer.ip_address,
        printer_port=printer.port_number,
        endpoint=tool_temperature_endpoint,
        api_key=printer.X_Api_Key,
        json=payload
    )

    if req.status_code == 409:
        raise ValidationError("The printer is not operational")

    return printer


def set_printer_chamber_temperature(printer_id: int, temperature: int) -> Printer:
    printer = get_printer(printer_id)

    if not check_if_printer_is_connected(printer):
        raise ServiceUnavailable("The printer is not connected, check your connection")

    if not printer.has_heated_chamber:
        raise ValidationError("The printer has no heated chamber")

    chamber_temperature_endpoint = "/api/printer/chamber"

    payload = {
        "command": "target",
        "target": temperature
    }

    req = issue_command_to_printer(
        printer_ip=printer.ip_address,
        printer_port=printer.port_number,
        endpoint=chamber_temperature_endpoint,
        api_key=printer.X_Api_Key,
        json=payload
    )

    if req.status_code == 409:
        raise ValidationError("The printer is not operational")

    return printer


def create_queue(printer: int, printing_models: OrderedDict) -> Queue:
    """Service for creating queues"""
    printer_object = Printer.objects.get(id=printer)
    queue = Queue.objects.create(printer=printer_object)
    queue.printing_models.set(flatten_list(printing_models.values()))
    queue.save()

    # since the queue is save, let's notify our printing manager that it should make use of it
    PrinterIOConfig.printing_manager.get_new_queue(queue, queue.printer)

    return queue


def delete_queue(queue: Queue) -> None:
    """Service that handles deletion of the queue"""
    queue.delete()


def add_models_to_queue(queue: Queue, models_to_add: dict) -> Queue:
    """Service for adding models to the queue without re-adding existing ones"""
    for model in flatten_list(models_to_add.values()):
        queue.printing_models.add(model.id)

    queue.save()

    # since the queue has been updated, we should let the printer manager know that something's changed

    PrinterIOConfig.printing_manager.refresh_queue(queue, queue.printer)

    return queue


def remove_models_from_queue(queue: Queue, models_to_remove: dict) -> Queue:
    """Service for removing given models from the queue"""
    for model in flatten_list(models_to_remove.values()):
        queue.printing_models.remove(model.id)

    queue.save()

    # since the queue has been updated, we should let the printer manager know that something's changed

    PrinterIOConfig.printing_manager.refresh_queue(queue, queue.printer)

    return queue


def check_if_printer_is_connected(printer_to_check: Printer) -> bool:
    """Service for checking whether or not the printer in question if actually connected"""
    connection_endpoint = "/api/connection"
    # The connection should read Operational
    try:
        req = requests.get(
            url="http://{ip}:{port}{endpoint}".format(
                ip=printer_to_check.ip_address,
                port=printer_to_check.port_number,
                endpoint=connection_endpoint
            ),
            headers={
                "X-Api-Key": printer_to_check.X_Api_Key,
                "Content-Type": "application/json"
            }
        )

        if not req.json()["current"]["state"] == "Operational":
            return False

    except ConnectionError:
        return False

    return True
