from printerIO.models import Queue, Printer
from printerIO.utils import flatten_list
from printerIO.selectors import get_printer
from collections import OrderedDict
import requests


def execute_gcode_command(printer_id:int, command:str) -> None:
    printer = get_printer(printer_id)
    command = command
    command_endpoint = "/api/printer/command"


    req = requests.post("http://{ip}:{port}{endpoint}".format(
        ip=printer.ip_address,
        port=printer.port_number,
        endpoint=command_endpoint
    ),
                        headers={"X-Api-Key":printer.X_Api_Key,
                                 "Content-Type":"application/json"},
                        json={"command":command},)
    

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
