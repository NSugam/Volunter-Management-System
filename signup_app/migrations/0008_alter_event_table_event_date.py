# Generated by Django 4.0.6 on 2022-08-22 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup_app', '0007_remove_registration_event_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_table',
            name='event_date',
            field=models.DateField(),
        ),
    ]
