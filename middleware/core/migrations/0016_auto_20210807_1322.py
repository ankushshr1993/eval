# Generated by Django 3.1.7 on 2021-08-07 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_node_host_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='host_enabled',
            field=models.BooleanField(default=True, verbose_name='Enable host to forward calls'),
        ),
    ]