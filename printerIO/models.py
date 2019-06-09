from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Printer(models.Model):
    objects = models.Manager()
    name = models.TextField()
    thumbnail = models.ImageField(upload_to="Images/", default="Images/Group_21.png")
    build_volume = models.TextField()
    printer_type = models.CharField(
        max_length=2,
        choices=(
            ("CR", "Cartesian"),
            ("DL", "Delta")
        ),
        default="CR"
    )
    ip_address = models.GenericIPAddressField(default="0.0.0.0")
    port_number = models.IntegerField(default=5000)
    is_printing = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    number_of_extruders = models.IntegerField(default=1)
    has_heated_chamber = models.BooleanField(default=False)
    X_Api_Key = models.TextField(default="")

    def __str__(self):
        return '{name} of type {type}'.format(name=self.name,
                                              type=self.printer_type)


class PrintingModel(models.Model):
    objects = models.Manager()
    file = models.FileField()
    name = models.TextField()
    thing_dimensions = models.TextField()

    def __str__(self):
        return self.name


class Queue(models.Model):
    objects = models.Manager()
    printer = models.OneToOneField(
        Printer,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    printing_models = models.ManyToManyField(PrintingModel)

    def __str__(self):
        return "models to be printed with " + self.printer.name


class PrintedModelQuality(models.Model):
    objects = models.Manager()
    printer = models.ForeignKey(Printer,
                                related_name="used_printer",
                                on_delete=models.CASCADE)
    model = models.ForeignKey(PrintingModel,
                              related_name="used_model",
                              on_delete=models.CASCADE)
    quality_number = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    was_cancelled = models.BooleanField(default=False)
