# Generated by Django 4.1.1 on 2022-10-08 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_remove_reserve_date_reserve_date_end_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reserve',
            old_name='date_end',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='reserve',
            old_name='date_start',
            new_name='start_date',
        ),
    ]