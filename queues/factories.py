import factory
from faker import Factory as FakerFactory
from printerIO.factiories import PrinterFactory
from printerIO.models import Queue

faker = FakerFactory.create()


class QueueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Queue

    printer = factory.SubFactory(PrinterFactory)

    @factory.post_generation
    def printing_models(self, create, extracted, **kwargs):

        if not create:
            # not needed here, we still need to cover it
            return

        if extracted:
            for model in extracted:
                self.printing_models.add(model)
