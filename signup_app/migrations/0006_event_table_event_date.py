# Generated by Django 4.0.6 on 2022-08-22 16:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup_app', '0005_alter_event_table_event_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_table',
            name='event_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
