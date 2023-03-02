# Generated by Django 3.1.5 on 2021-02-08 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_node_host_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='host_user',
            field=models.CharField(default='user33705', max_length=30, verbose_name='Give userid for function calls'),
        ),
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('called_function', models.CharField(max_length=300, verbose_name='Give function name')),
                ('called_delay', models.FloatField(verbose_name='Function Latency')),
                ('called_url', models.CharField(max_length=30, verbose_name='Url Called')),
                ('recent_call', models.DateTimeField(auto_now=True)),
                ('reply_call', models.DateTimeField(auto_now=True)),
                ('called_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.node')),
            ],
        ),
    ]
