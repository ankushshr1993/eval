# Generated by Django 3.1.7 on 2021-08-11 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20210811_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='description',
            field=models.TextField(blank=True, max_length=255, verbose_name='Experiment description'),
        ),
    ]
