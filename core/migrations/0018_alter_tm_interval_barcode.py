# Generated by Django 4.0.2 on 2022-06-14 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_tm_interval_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tm_interval',
            name='barcode',
            field=models.ImageField(blank=True, null=True, upload_to='barcodeImages'),
        ),
    ]
