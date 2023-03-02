# Generated by Django 3.1.5 on 2021-03-07 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210209_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='host_kf_cpu',
            field=models.FloatField(default=0, verbose_name='KF cpu'),
        ),
        migrations.AddField(
            model_name='node',
            name='host_kf_memory',
            field=models.FloatField(default=0, verbose_name='KF memory'),
        ),
        migrations.AddField(
            model_name='node',
            name='host_kf_rx',
            field=models.FloatField(default=0, verbose_name='KF Rx'),
        ),
        migrations.AddField(
            model_name='node',
            name='host_kf_tx',
            field=models.FloatField(default=0, verbose_name='KF Tx'),
        ),
    ]
