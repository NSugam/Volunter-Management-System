from django.db import models

class Event_table(models.Model):
    event_id = models.AutoField
    event_name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    event_price = models.IntegerField(default=0)
    def __str__(self):
        return self.event_name

class Registration(models.Model):
    username = models.CharField(max_length=100)
    firstname = models.CharField(max_length=20)
    event_name = models.CharField(max_length=20)
    event_price = models.IntegerField(default=0)
    def __str__(self):
        return self.username