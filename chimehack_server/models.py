from django.db import models

class Setting(models.Model):
    cellphone = models.CharField(max_length=100)
    emergencyContact = models.CharField(max_length=100)
    SMS = models.CharField(max_length=100)
    MMS = models.CharField(max_length=100)
    redAlertContact = models.CharField(max_length=100)
    secretKey = models.CharField(max_length=100)
    dailyMessage = models.CharField(max_length=100)
