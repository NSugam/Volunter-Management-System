from django.db import models

class New_Event(models.Model):
    event_id = models.AutoField
    event_name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    event_price = models.IntegerField()

    def __str__(self):
        return self.event_name
