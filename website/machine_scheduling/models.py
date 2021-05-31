from django.db import models
import datetime
# Create your models here.

class Document(models.Model):
    date = models.DateField(primary_key = True)
    file = models.FileField(upload_to = 'documents/raw_data')
    schedule_is_done = models.BooleanField(default = False)
    def __str__(self) :
        return str(self.date)
    class Meta :
        ordering = ('date' ,)

class StrongMachineInfo(models.Model):
    index = models.IntegerField(primary_key = True)
    startTime = models.TimeField(default = datetime.time(hour = 8))

class WeakMachineInfo(models.Model):
    index = models.IntegerField(primary_key = True)
    startTime = models.TimeField(default = datetime.time(hour = 8))