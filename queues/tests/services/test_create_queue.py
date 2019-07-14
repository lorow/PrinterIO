from printerIO.factiories import PrinterFactory, PrintingModelFactory
from queues.selectors import get_queue_by_queue_id
from queues.services import create_queue
from collections import OrderedDict
from django.test import TestCase


class CreateQueueTest(TestCase):

    def setUp(self):
        self.printer = PrinterFactory()
        self.printing_models = OrderedDict()
        self.printing_models['printing_models'] = [
            PrintingModelFactory(),
            PrintingModelFactory()
        ]

        self.service = create_queue

    def test_whether_the_queue_is_being_created(self):
        """test whether or not the created queue is the same as the one in the database"""
        queue = self.service(self.printer.id, self.printing_models)
        self.assertEquals(queue, get_queue_by_queue_id(queue.printer.id))
