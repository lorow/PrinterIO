from printers.services import set_printer_temperature
from rest_framework.exceptions import ValidationError
from printers.exceptions import ServiceUnavailable
from printerIO.factories import PrinterFactory
import responses
import pytest
pytestmark = pytest.mark.django_db


@pytest.fixture
def printer_fixture():
    return PrinterFactory()


class TestSetPrinterTemperature:

    def test_set_printer_bed_temperature(self, printer_fixture):
        """
            This will fail when the fucntion raises either ValidationError
            or ServiceUnavailable due to
            the fact that we can't do: with not pytest.raises()
        """
        with responses.RequestsMock() as resp:
            # we need to mock the connection test first
            resp.add(
                resp.GET,
                f'http://{printer_fixture.ip_address}:{printer_fixture.port_number}/api/connection',
                json={"current": {"state": "Operational"}}
            )
            # then we can mock the tool connection
            resp.add(
                resp.POST, 'http://{printer_ip}:{printer_port}/api/printer/bed'.format(
                    printer_ip=printer_fixture.ip_address,
                    printer_port=printer_fixture.port_number
                ),
                adding_headers={
                    "X-Api-Key": printer_fixture.X_Api_Key,
                    "Content-Type": "application/json"
                },
                json={
                    "command": "target",
                    "target": [60]
                },
                status=200
            )

            set_printer_temperature(
                printer_fixture.pk,
                "bed",
                [60]
            )
