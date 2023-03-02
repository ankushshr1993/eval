# Generated by Django 3.1.7 on 2021-08-07 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_requestlog_pred_cpu_variance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestlog',
            name='pred_cpu_variance',
        ),
        migrations.AddField(
            model_name='node',
            name='host_kf_cpu_variance',
            field=models.FloatField(default=0, verbose_name='KF Uncertainty cpu'),
        ),
    ]
