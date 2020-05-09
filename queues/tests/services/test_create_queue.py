from printerIO.tests.factories import PrinterFactory, PrintingModelFactory
from queues.selectors import get_queue_by_queue_id, get_all_queues
from queues.services import (
    create_queue,
    delete_queue,
    add_models_to_queue,
    remove_models_from_queue,
)
import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def queue_fixture():
    printer = PrinterFactory()
    models_to_print = [
        PrintingModelFactory(),
        PrintingModelFactory(),
        PrintingModelFactory(),
    ]
    return create_queue(printer.id, models_to_print)


class TestQueueServices:
    def test_create_queue(self):

        printer = PrinterFactory()
        models_to_print = [
            PrintingModelFactory(),
            PrintingModelFactory(),
            PrintingModelFactory(),
        ]
        created_queue = create_queue(printer.id, models_to_print)

        assert created_queue == get_queue_by_queue_id(created_queue.pk)

    def test_delete_queue(self, queue_fixture):
        delete_queue(queue_fixture)

        assert list(get_all_queues()) == []

    def test_add_models_to_queue(self, queue_fixture):
        model_to_add = PrintingModelFactory()
        new_queue = add_models_to_queue(queue_fixture, [model_to_add,])

        assert model_to_add in new_queue.printing_models.all()

    def test_remove_models_from_queue(self, queue_fixture):
        model_to_add = PrintingModelFactory()
        new_queue = remove_models_from_queue(queue_fixture, [model_to_add,])

        assert model_to_add not in new_queue.printing_models.all()
