# Generated by Django 3.1.7 on 2021-08-06 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210722_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestlog',
            name='called_url',
            field=models.CharField(max_length=150, verbose_name='Url Called'),
        ),
    ]