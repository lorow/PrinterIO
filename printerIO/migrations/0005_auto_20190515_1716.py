# Generated by Django 2.1.1 on 2019-05-15 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printerIO', '0004_queue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queue',
            old_name='objects',
            new_name='objects_to_print',
        ),
    ]
