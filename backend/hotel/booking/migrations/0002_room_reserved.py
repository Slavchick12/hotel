# Generated by Django 4.1.1 on 2022-10-03 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='reserved',
            field=models.BooleanField(default=False),
        ),
    ]