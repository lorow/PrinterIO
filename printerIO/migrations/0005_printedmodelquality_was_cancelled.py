# Generated by Django 2.1.1 on 2019-06-09 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printerIO', '0004_printer_is_paused'),
    ]

    operations = [
        migrations.AddField(
            model_name='printedmodelquality',
            name='was_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]