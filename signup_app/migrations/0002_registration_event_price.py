# Generated by Django 4.0.6 on 2022-08-21 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='event_price',
            field=models.CharField(default='abcd', max_length=20),
        ),
    ]