from printerIO.services import check_if_printer_is_connected
from printerIO.factiories import PrinterFactory
from printerIO.models import Printer
from django.test import TestCase
import responses


class PrinterConnectionCheckingTests(TestCase):

    def setUp(self) -> None:
        self.service = check_if_printer_is_connected
        self.printer = PrinterFactory()

    def test_check_if_printer_is_conneted_fails_due_to_no_connection(self) -> None:
        """Tests whether or not the connection-checking service will return False as to
            the current state of the printer is other than Operational and thus not connected
        """
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET, 'http://{printer_ip}:{printer_port}/api/connection'.format(
                    printer_ip=self.printer.ip_address,
                    printer_port=self.printer.port_number
                ),
                json={"current": {"state": "Disconnected"}}
            )

            self.assertFalse(self.service(self.printer))

    def test_check_if_printer_is_connected_passes_due_to_existing_connection(self) -> None:
        """Tests whether or not the connection-checking service will return True
            as to the connection between octoprint and the printer itself is Operational
        """

        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET, 'http://{printer_ip}:{printer_port}/api/connection'.format(
                    printer_ip=self.printer.ip_address,
                    printer_port=self.printer.port_number
                ),
                json={"current": {"state": "Operational"}}
            )

            self.assertTrue(self.service(self.printer))

    def test_check_if_printer_is_connected_fails_due_to_server_being_offline(self) -> None:
        """Tests whether or not the connection-checking service will return False
            as to the connection attempt failing due to server being offline
        """

        self.assertFalse(self.service(self.printer))
