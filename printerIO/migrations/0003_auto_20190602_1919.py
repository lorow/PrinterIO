# Generated by Django 2.1.1 on 2019-06-02 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printerIO', '0002_auto_20190528_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='printer',
            name='password',
        ),
        migrations.RemoveField(
            model_name='printer',
            name='username',
        ),
        migrations.AddField(
            model_name='printer',
            name='X_Api_Key',
            field=models.TextField(default=''),
        ),
    ]
