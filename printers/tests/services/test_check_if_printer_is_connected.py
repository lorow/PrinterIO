from printers.services import check_if_printer_is_connected
from printerIO.tests.factories import PrinterFactory
from printers.exceptions import ServiceUnavailable
import responses
import pytest

pytestmark = pytest.mark.django_db


class TestPrinterConnectionService:
    def test_check_if_printer_is_connected_fails_due_to_no_connection(self) -> None:
        """
            Tests whether or not the connection-checking
            service will return False as to the current state of
            the printer is other than Operational and thus not connected
        """
        printer = PrinterFactory()
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                "http://{printer_ip}:{printer_port}/api/connection".format(
                    printer_ip=printer.ip_address, printer_port=printer.port_number
                ),
                json={"current": {"state": "Disconnected"}},
            )

            assert not check_if_printer_is_connected(printer)

    def test_check_if_printer_is_connected_passes(self) -> None:
        """
        Tests whether or not the connection-checking
        service will return True as to the connection
        between octoprint and the printer itself is Operational
        """
        printer = PrinterFactory()
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                "http://{printer_ip}:{printer_port}/api/connection".format(
                    printer_ip=printer.ip_address, printer_port=printer.port_number
                ),
                json={"current": {"state": "Operational"}},
            )

            assert check_if_printer_is_connected(printer)

    def test_check_if_printer_is_connected_fails_due_to_server_being_offline(
        self,
    ) -> None:
        """
        Tests whether or not the connection-checking service will return False
        as to the connection attempt failing due to server being offline
        """

        with pytest.raises(ServiceUnavailable):
            check_if_printer_is_connected(PrinterFactory())
