# Generated by Django 3.1.5 on 2021-02-08 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210208_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestlog',
            name='called_filter',
            field=models.CharField(default='linear', max_length=30, verbose_name='Method'),
        ),
        migrations.AddField(
            model_name='requestlog',
            name='called_method',
            field=models.CharField(default='GET', max_length=30, verbose_name='Method'),
        ),
    ]
