from collections import OrderedDict
import requests


class PrintingManager:

    def __init__(self):
        self.current_queues = {}

    def refresh_queue(self, queue, printer):
        """refreshes the queue identified by the printer id"""
        self.current_queues[printer] = list(queue.printing_models.all())

    def get_new_queue(self, queue, printer):
        """adds queue to the current_queues and automatically calls the print"""
        self.current_queues[printer] = list(queue.printing_models.all())
        self.print(printer)

    def print(self, printer):
        """When called, pops model from the list of models identified by printer and sends it to the octoprint
        instance
        """

        if self.__check_local_queue(printer):
            # if the queue isn't empty, simply proceed with printing
            model = self.current_queues[printer].pop()
            self.remove_model_from_queue(printer, model)
            self.issue_printing_command(printer, model)

            printer.is_printing = True
            printer.save()

    def __check_local_queue(self, printer):
        if printer in self.current_queues:
            if len(self.current_queues[printer]):
                return True

        return False

    def next_job(self, printer):
        """Check the state of the queue, and calls the next printing job if possible"""

        if printer in self.current_queues:
            if not len(self.current_queues[printer]):
                del self.current_queues[printer]
                self.clean_queue(printer)

            else:
                self.print(printer)

    @staticmethod
    def remove_model_from_queue(printer, model):
        """removes the model from the queue"""

        from printerIO.services import remove_models_from_queue
        from printerIO.selectors import get_queue_by_printer_id

        models_to_delete = OrderedDict()
        models_to_delete["printing_models"] = [model]

        queue = get_queue_by_printer_id(printer.id)
        remove_models_from_queue(queue, models_to_delete)

    @staticmethod
    def clean_queue(printer):
        """deletes the queue"""

        from printerIO.selectors import get_queue_by_printer_id
        from printerIO.services import delete_queue

        queue = get_queue_by_printer_id(printer.id)
        delete_queue(queue)

    @staticmethod
    def issue_printing_command(printer, model):
        """Sends actual requests to the octoprint instance"""
        from printerIO.utils import issue_command_to_printer
        # TODO make it so user chooses where to send the files -> PrintingModel
        file_endpoint = "/api/files/local"

        file = open("media/{file_name}".format(file_name=model.file), 'rb')
        file_req = requests.post(
            url="http://{ip}:{port}{endpoint}".format(
                ip=printer.ip_address,
                port=printer.port_number,
                endpoint=file_endpoint
            ),
            headers={
                "X-Api-Key": printer.X_Api_Key
            },
            files={'file': file, 'name': model.file}
        )
        # the upload had worked, we may proceed
        if file_req.status_code == 201:

            select_and_print_file_endpoint = "/api/files/local/{filename}".format(filename=model.file)
            issue_command_to_printer(
                printer_ip=printer.ip_address,
                printer_port=printer.port_number,
                endpoint=select_and_print_file_endpoint,
                api_key=printer.X_Api_Key,
                json={"command": "select",
                      "print": True}
            )
