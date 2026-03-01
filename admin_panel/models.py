from django.db import models
from doctor.models import Doctor
from patient.models import Patient


class Schedule(models.Model):
    scheduleid = models.AutoField(primary_key=True)
    docid = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='docid')
    title = models.CharField(max_length=255)
    scheduledate = models.DateField()
    scheduletime = models.TimeField()
    nop = models.IntegerField()

    class Meta:
        db_table = 'schedule'

    def __str__(self):
        return self.title


class Appointment(models.Model):
    appoid = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='pid')
    apponum = models.IntegerField()
    scheduleid = models.ForeignKey(Schedule, on_delete=models.CASCADE, db_column='scheduleid')
    appodate = models.DateField()

    class Meta:
        db_table = 'appointment'

    def __str__(self):
        return f"Appointment {self.appoid}"
