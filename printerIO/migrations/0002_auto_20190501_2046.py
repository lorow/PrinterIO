# Generated by Django 2.1.5 on 2019-05-01 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printerIO', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='printer',
            name='ip_address',
            field=models.GenericIPAddressField(default='0.0.0.0'),
        ),
        migrations.AddField(
            model_name='printer',
            name='port_number',
            field=models.IntegerField(default=5000),
        ),
    ]
