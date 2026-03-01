from django.db import models
from accounts.models import WebUser


class Patient(models.Model):
    pid = models.AutoField(primary_key=True)
    pemail = models.OneToOneField(WebUser, on_delete=models.CASCADE, db_column='pemail')
    pname = models.CharField(max_length=255)
    ppassword = models.CharField(max_length=255)
    paddress = models.CharField(max_length=255)
    pnic = models.CharField(max_length=255)
    ptel = models.CharField(max_length=255)
    pdob = models.DateField()

    class Meta:
        db_table = 'patient'

    def __str__(self):
        return self.pname
