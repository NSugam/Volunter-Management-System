# Generated by Django 4.0.6 on 2022-08-21 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup_app', '0002_registration_event_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='event_price',
            field=models.CharField(default='', max_length=20),
        ),
    ]