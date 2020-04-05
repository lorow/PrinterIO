from printers.services import set_printer_tool_temperature
from rest_framework.exceptions import ValidationError
from printers.exceptions import ServiceUnavailable
from printerIO.factories import PrinterFactory
from django.test import TestCase
import responses
import pytest
pytestmark = pytest.mark.django_db


# class PrinterToolTemperatureChangingServiceTests(TestCase):

#     def setUp(self) -> None:
#         self.printer = PrinterFactory()
#         self.service = set_printer_tool_temperature
#         self.temperatures = [120]
#         self.temperatures_outmatching_the_number_of_extruders = [120, 30]

#     def test_set_printer_tool_temperature_fail_due_to_no_connection(self) -> None:

#         with self.assertRaises(ServiceUnavailable):
#             self.service(self.printer.id, self.temperatures)

#     def test_if_printer_tool_temperature_raises_ValidationError(self) -> None:

#         with responses.RequestsMock() as resp:
#             resp.add(
#                 resp.GET, 'http://{printer_ip}:{printer_port}/api/connection'.format(
#                     printer_ip=self.printer.ip_address,
#                     printer_port=self.printer.port_number
#                 ),
#                 json={"current": {"state": "Operational"}}
#             )

#             resp.add(
#                 resp.POST, 'http://{printer_ip}:{printer_port}/api/printer/tool'.format(
#                     printer_ip=self.printer.ip_address,
#                     printer_port=self.printer.port_number
#                 ),
#                 adding_headers={
#                     "X-Api-Key": self.printer.X_Api_Key,
#                     "Content-Type": "application/json"
#                 },
#                 json={
#                     "command": "target",
#                     "target": self.temperatures
#                 },
#                 status=409
#             )

#             with self.assertRaises(ValidationError):
#                 self.service(self.printer.id, self.temperatures)

#     def test_if_printer_tool_temperature_fails_due_to_having_too_many_temperatures_provided(self) -> None:

#         with responses.RequestsMock() as resp:
#             resp.add(
#                 resp.GET, 'http://{printer_ip}:{printer_port}/api/connection'.format(
#                     printer_ip=self.printer.ip_address,
#                     printer_port=self.printer.port_number
#                 ),
#                 json={"current": {"state": "Operational"}}
#             )

#             resp.add(
#                 resp.POST, 'http://{printer_ip}:{printer_port}/api/printer/tool'.format(
#                     printer_ip=self.printer.ip_address,
#                     printer_port=self.printer.port_number
#                 ),
#                 adding_headers={
#                     "X-Api-Key": self.printer.X_Api_Key,
#                     "Content-Type": "application/json"
#                 },
#                 json={
#                     "command": "target",
#                     "target": self.temperatures_outmatching_the_number_of_extruders
#                 },
#                 status=409
#             )

#             with self.assertRaises(ValidationError):
#                 self.service(self.printer.id, self.temperatures)

#     def test_printer_tool_temperature_returns_printer_and_passes(self):

#         with responses.RequestsMock() as resp:
#             resp.add(
#                 resp.GET, 'http://{printer_ip}:{printer_port}/api/connection'.format(
#                     printer_ip=self.printer.ip_address,
#                     printer_port=self.printer.port_number
#                 ),
#                 json={"current": {"state": "Operational"}}
#             )

#             resp.add(
#                 resp.POST, 'http://{printer_ip}:{printer_port}/api/printer/tool'.format(
#                     printer_ip=self.printer.ip_address,
#                     printer_port=self.printer.port_number
#                 ),
#                 adding_headers={
#                     "X-Api-Key": self.printer.X_Api_Key,
#                     "Content-Type": "application/json"
#                 },
#                 json={
#                     "command": "target",
#                     "target": self.temperatures
#                 },
#                 status=200
#             )
#             printer = self.service(self.printer.id, self.temperatures)

#             self.assertEqual(printer, self.printer)
