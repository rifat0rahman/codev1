# Generated by Django 3.2.6 on 2022-03-24 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_intervaltwenty2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intervaltwenty2',
            name='name',
            field=models.CharField(default='60', max_length=50),
        ),
    ]
