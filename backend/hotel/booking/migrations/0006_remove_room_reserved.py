# Generated by Django 4.1.1 on 2022-10-03 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_alter_reserve_options_reserve_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='reserved',
        ),
    ]
