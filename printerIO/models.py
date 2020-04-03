from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.db import models


# we will support only FDM printers for a while, so no resin just yet
class Filament(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=250, default="")
    producer = models.CharField(max_length=250, default="")
    colour = models.CharField(max_length=100, default="")
    diameter = models.FloatField(
        max_length=5,
        choices=(
            (1.75, "1.75mm diameter"),
            (3, "3mm diameter")
        ),
        default=1.75)
    weight = models.FloatField(default=1)  # in kilos, so 0.6KG or 1KG
    filament_left = models.FloatField(default=1)  # also in kilos
    filament_type = models.CharField(max_length=250, default="PLA")
    price = models.FloatField()


class Printer(models.Model):
    objects = models.Manager()
    name = models.TextField()
    thumbnail = models.ImageField(
        upload_to="Images/", default="Images/Group_21.png")
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

    filament = models.ManyToManyField(Filament, blank=True)

    def __str__(self):
        return '{name} of type {type}'.format(
            name=self.name,
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
    model = models.ForeignKey(
        PrintingModel,
        related_name="used_model",
        on_delete=models.CASCADE)
    quality_number = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    was_cancelled = models.BooleanField(default=False)


class TaskCategory(models.Model):
    name = models.CharField(max_length=100)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    created = models.DateField(default=timezone.now)
    due = models.DateField(default=timezone.now, blank=True)
    category = models.ForeignKey(
        TaskCategory,
        on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Problem(models.Model):
    objects = models.Manager()
    severity = models.IntegerField(
        validators=[MaxValueValidator(3), MinValueValidator(1)]
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateField(default=timezone.now)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.title
