# Generated by Django 4.0.6 on 2022-08-21 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup_app', '0004_alter_registration_event_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_table',
            name='event_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='registration',
            name='event_price',
            field=models.IntegerField(default=0),
        ),
    ]
