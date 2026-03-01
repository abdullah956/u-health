from django.db import models
from accounts.models import WebUser


class Specialties(models.Model):
    id = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=255)

    class Meta:
        db_table = 'specialties'

    def __str__(self):
        return self.sname


class Doctor(models.Model):
    docid = models.AutoField(primary_key=True)
    docemail = models.OneToOneField(WebUser, on_delete=models.CASCADE, db_column='docemail')
    docname = models.CharField(max_length=255)
    docpassword = models.CharField(max_length=255)
    docnic = models.CharField(max_length=255)
    doctel = models.CharField(max_length=255)
    specialties = models.ForeignKey(Specialties, on_delete=models.CASCADE)

    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return self.docname
