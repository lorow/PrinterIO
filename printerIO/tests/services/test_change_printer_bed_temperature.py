from printerIO.services import set_printer_bed_temperature
from rest_framework.exceptions import ValidationError
from printerIO.exceptions import ServiceUnavailable
from printerIO.factiories import PrinterFactory
from django.test import TestCase
import responses


class PrinterBedTemperatureChangingServiceTests(TestCase):

    def setUp(self) -> None:
        self.printer = PrinterFactory()
        self.service = set_printer_bed_temperature
        self.temperature = 120

    def test_set_printer_bed_temperature_fail_due_to_no_connection(self) -> None:

        with self.assertRaises(ServiceUnavailable):
            self.service(self.printer.id, self.temperature)

    def test_if_printer_bed_temperature_raises_ValidationError(self) -> None:

        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET, 'http://{printer_ip}:{printer_port}/api/connection'.format(
                    printer_ip=self.printer.ip_address,
                    printer_port=self.printer.port_number
                ),
                json={"current": {"state": "Operational"}}
            )

            resp.add(
                resp.POST, 'http://{printer_ip}:{printer_port}/api/printer/bed'.format(
                    printer_ip=self.printer.ip_address,
                    printer_port=self.printer.port_number
                ),
                adding_headers={
                    "X-Api-Key": self.printer.X_Api_Key,
                    "Content-Type": "application/json"
                },
                json={"command": "target",
                      "target": self.temperature
                      },
                status=409
            )

            with self.assertRaises(ValidationError):
                self.service(self.printer.id, self.temperature)

    def test_printer_bed_temperature_returns_printer_and_passes(self):

        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET, 'http://{printer_ip}:{printer_port}/api/connection'.format(
                    printer_ip=self.printer.ip_address,
                    printer_port=self.printer.port_number
                ),
                json={"current": {"state": "Operational"}}
            )

            resp.add(
                resp.POST, 'http://{printer_ip}:{printer_port}/api/printer/bed'.format(
                    printer_ip=self.printer.ip_address,
                    printer_port=self.printer.port_number
                ),
                adding_headers={
                    "X-Api-Key": self.printer.X_Api_Key,
                    "Content-Type": "application/json"
                },
                json={"command": "target",
                      "target": self.temperature
                      },
                status=200
            )
            printer = self.service(self.printer.id, self.temperature)

            self.assertEqual(printer, self.printer)
