# Generated by Django 3.0.5 on 2020-08-28 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baliza', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historialrssi',
            options={'ordering': ['-fechaRegistro'], 'verbose_name': 'Historial RSSI', 'verbose_name_plural': 'Historials RSSI'},
        ),
    ]