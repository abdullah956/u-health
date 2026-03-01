from django.db import models


class WebUser(models.Model):
    USER_TYPES = [
        ('a', 'Admin'),
        ('d', 'Doctor'),
        ('p', 'Patient'),
    ]

    email = models.CharField(max_length=255, primary_key=True)
    usertype = models.CharField(max_length=1, choices=USER_TYPES)

    class Meta:
        db_table = 'webuser'

    def __str__(self):
        return self.email


class Admin(models.Model):
    aemail = models.OneToOneField(WebUser, on_delete=models.CASCADE, primary_key=True, db_column='aemail')
    apassword = models.CharField(max_length=255)

    class Meta:
        db_table = 'admin'

    def __str__(self):
        return str(self.aemail)
