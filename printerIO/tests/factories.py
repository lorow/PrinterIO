from django.core.files import File
from printerIO.models import *
from faker import Factory
import random
import factory


faker = Factory.create()


class PrinterFactory(factory.DjangoModelFactory):
    class Meta:
        model = Printer

    name = faker.name()
    build_volume = "{x}x{y}x{z}".format(
        x=random.randint(0, 999), y=random.randint(0, 999), z=random.randint(0, 999)
    )
    ip_address = faker.ipv4()
    port_number = random.randint(1, 9000)
    X_Api_Key = faker.password(
        length=15, special_chars=True, digits=True, upper_case=True, lower_case=True
    )


class PrintingModelFactory(factory.DjangoModelFactory):
    class Meta:
        model = PrintingModel

    file = File(
        open("media/JA5A5S_3dbenchy-1_VntpwQf.gcode")
    )  # TODO make it so it generates its own fake files
    name = faker.file_name(extension="gcode")
    thing_dimensions = "{x}x{y}x{z}".format(
        x=random.randint(0, 150), y=random.randint(0, 150), z=random.randint(0, 150)
    )
