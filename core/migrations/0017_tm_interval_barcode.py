# Generated by Django 4.0.2 on 2022-06-14 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_rename_twentym_tm_interval'),
    ]

    operations = [
        migrations.AddField(
            model_name='tm_interval',
            name='barcode',
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
    ]