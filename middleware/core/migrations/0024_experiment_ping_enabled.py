# Generated by Django 3.1.7 on 2021-09-10 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20210906_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='ping_enabled',
            field=models.BooleanField(default=False, verbose_name='Ping enabled/disabled'),
        ),
    ]
