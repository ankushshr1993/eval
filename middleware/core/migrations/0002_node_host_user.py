# Generated by Django 3.1.5 on 2021-01-28 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='host_user',
            field=models.CharField(default='user563112', max_length=30, verbose_name='Give userid for function calls'),
        ),
    ]
