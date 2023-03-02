# Generated by Django 3.1.7 on 2021-09-06 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20210827_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='host_kf_ping',
            field=models.FloatField(default=0, verbose_name='KF Ping Value'),
        ),
        migrations.AddField(
            model_name='node',
            name='host_ping',
            field=models.FloatField(default=0, verbose_name='Ping Value'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='n_nodes',
            field=models.IntegerField(default=2, verbose_name='Number of enabled Nodes'),
        ),
        migrations.AlterField(
            model_name='nodelogvalue',
            name='host_ire_cpu',
            field=models.FloatField(default=0, verbose_name='Measured cpu Ireland'),
        ),
        migrations.AlterField(
            model_name='nodelogvalue',
            name='host_ire_kf_cpu',
            field=models.FloatField(default=0, verbose_name='KF cpu Ireland'),
        ),
    ]
