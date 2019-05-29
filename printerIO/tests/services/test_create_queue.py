from django.test import TestCase
from printerIO.models import Printer, PrintingModel
from printerIO.selectors import get_queue
from printerIO.services import create_queue
from django.core.files import File
from collections import OrderedDict


class CreateQueueTest(TestCase):

    def setUp(self):
        file1 = File(open("media/JA5A5S_3dbenchy-1_VntpwQf.gcode"))
        file2 = File(open("media/JA5A5S_3dbenchy-1.gcode"))

        self.printer = Printer.objects.create(
            name="Testing printer",
            build_volume="300x300x300"
        )
        self.printing_models = OrderedDict()
        self.printing_models['printing_models'] = [
            PrintingModel.objects.create(
                file=file1,
                name="test.gcode",
                thing_dimensions="30x30x30"
            ),
            PrintingModel.objects.create(
                file=file2,
                name="test23.gcode"
            )
        ]

        self.service = create_queue

    def test_whether_the_queue_is_being_created(self):
        """test whether or not the created queue is the same as the one in the database"""
        queue = self.service(self.printer.id, self.printing_models)
        self.assertEquals(queue, get_queue(1), "test")
