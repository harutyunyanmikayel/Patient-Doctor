from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    appointment_slots = models.ManyToManyField('PatientTime', blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class PatientTime(models.Model):
    appointment_time = models.DateTimeField()
