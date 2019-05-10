from django.db import models


class Printer(models.Model):
    name = models.TextField()
    thumbnail = models.ImageField(upload_to="Images/")
    build_volume = models.TextField()
    printer_type = models.CharField(
        max_length = 2,
        choices = (
            ("CR", "Cartesian"),
            ("DL", "Delta")
        ),
        default="CR"
    )
    ip_address = models.GenericIPAddressField(default="0.0.0.0")
    port_number = models.IntegerField(default=5000)
    is_printing = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " of type " + self.printer_type


class PrintingModel(models.Model):
    file = models.FileField()
    name = models.TextField()
    thing_dimensions = models.TextField()

    def __str__(self):
        return self.name


class Queue(models.Model):
    printer = models.OneToOneField(
        Printer,
        on_delete=models.CASCADE,
        primary_key=True
    )
    objects = models.ManyToManyField(PrintingModel)

    def __str__(self):
        return "models to be printed with " + self.printer.name
    
