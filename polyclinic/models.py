from datetime import timezone
from operator import mod
from tkinter.tix import Tree
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.manager import EmptyManager
from django.forms.widgets import Select
from django.utils import tree, timezone
from django import forms
from django.shortcuts import reverse

from polyclinic.managers import MedicalStaffManager

User = settings.AUTH_USER_MODEL
# Create your models here.
ROLES = [
    ('NoRole', 'NoRole'),
    ('Doctor', 'Doctor'),
    ('Patient', 'Patient'),
    ('Receptionist', 'Receptionist'),
    ('Admin', 'Admin'),
    ('Accountant', 'Accountant'),
    ('Nurse', 'Nurse'),
    ('Labtech', 'Labtech'),
    ('HRM', 'HRM'),
    ('Specialist', 'Specialist'),
    ('Ophtalmologist', 'Ophtalmologist'),
    ('Pharmacist', 'Pharmacist'),
    ('Dentist', 'Dentist'),
    ('Cashier', 'Cashier')
]

MessageType = [

    ('REPORT_PROBLEM', 'REPORT_PROBLEM'),
    ('HOSPITALISATION_REQUEST', 'HOSPITALISATION_REQUEST'),
    ('CONSULTATION_REQUEST', 'CONSULTATION_REQUEST'),
    ('ACCESS_REQUEST', 'ACCESS_REQUEST'),
    ('INFO', 'INFO'),

]

SEXE = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

CONDITION = [
    ('NoCritical', 'NoCritical'),
    ('Critical', 'Critical'),
]

SERVICE = [

    ('Generalist', 'Generalist'),
    ('Specialist', 'Specialist'),
    ('All', 'All'),

]


# ======================================
# ======================================== APPOINTMENT, MEDICALSTAFF, DEPARTMENT, PATIENT
# ======================================


class MedicalStaff(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLES, default='NoRole')
    cniNumber = models.CharField(max_length=20, blank=True, default=" ")  # The patient CNI
    gender = models.CharField(max_length=50, choices=SEXE, default='Male', blank=True)
    profile_picture = models.ImageField(upload_to='social/images', blank=True, null=True)

    objects = MedicalStaffManager()

    def __str__(self):
        return self.username


class Department(models.Model):
    name = models.CharField(max_length=50, blank=True)
    reference = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.reference


class PatientAccess(models.Model):
    givenAt = models.DateTimeField(auto_now=True, blank=True)
    lostAt = models.DateTimeField(auto_now=True, blank=True)

    access = models.BooleanField(default=True)

    idPatient = models.ForeignKey("Patient", on_delete=models.CASCADE, null=False)
    idMedicalStaff = models.ForeignKey("MedicalStaff", on_delete=models.CASCADE, null=False)


class Patient(models.Model):
    addDate = models.DateField(auto_now=True, blank=True)
    addTime = models.TimeField(auto_now=True, blank=True)
    cniNumber = models.CharField(max_length=20, blank=True, default=" ")  # The patient CNI
    firstName = models.CharField(max_length=50, blank=True)
    lastName = models.CharField(max_length=50, blank=True, default=" ")
    gender = models.CharField(max_length=50, choices=SEXE, default='Male', blank=True)  # The patient gender (M, F)
    phoneNumber = models.CharField(max_length=100, blank=True, default=" ")
    birthDate = models.DateField(blank=True, null=True, default="0000-00-00")
    address = models.CharField(max_length=25, blank=True, default=" ")
    email = models.CharField(max_length=25, blank=True, default=" ")
    condition = models.CharField(max_length=50, choices=CONDITION, default='NoCritical', null=False)
    service = models.CharField(max_length=50, choices=SERVICE, default='Generalist', null=False)
    status = models.CharField(max_length=20, default="invalid")  # The patient status

    idMedicalFolder = models.ForeignKey("MedicalFolder", on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.firstName.__str__() + ' ' + self.lastName.__str__()


class Appointment(models.Model):
    atDate = models.DateField(auto_now=False)
    reason = models.CharField(max_length=300)
    requirements = models.CharField(max_length=500)

    idPatient = models.ForeignKey("Patient", on_delete=models.CASCADE, null=False)
    idMedicalStaff = models.ForeignKey("MedicalStaff", on_delete=models.CASCADE, null=False)


# ======================================
# ======================================== PARAMETERS, APPOINTMENT, CONSULTATION, MEDICALFOLDER
# ======================================

class Parameters(models.Model):
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    arterialPressure = models.FloatField(blank=True, null=True)
    skinAppearance = models.CharField(max_length=100, blank=True, null=True)
    addTime = models.TimeField(auto_now=True)
    addDate = models.DateField(auto_now=True)

    idMedicalFolder = models.ForeignKey("MedicalFolder", on_delete=models.DO_NOTHING, null=True)
    idMedicalStaff = models.ForeignKey("MedicalStaff", on_delete=models.CASCADE, null=False)


class Consultation(models.Model):
    consultationDate = models.DateField(auto_now=True)
    consultationTime = models.TimeField(auto_now=True)
    consultationCost = models.FloatField(blank=True, null=True)
    consultationReason = models.CharField(max_length=100, blank=True)
    consultationNotes = models.TextField(blank=True, null=True, max_length=100000)

    allergy = models.CharField(max_length=1000, null=True, blank=True)
    previousHistory = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, default="invalid")

    idParameters = models.ForeignKey("Parameters", on_delete=models.CASCADE, null=False)
    idMedicalFolderPage = models.ForeignKey("MedicalFolderPage", on_delete=models.CASCADE, null=False)
    idPatient = models.ForeignKey("Patient", on_delete=models.CASCADE, null=False, blank=True)
    idMedicalStaff = models.ForeignKey("MedicalStaff", on_delete=models.CASCADE, null=False)
    idConsultationType = models.ForeignKey("ConsultationType", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.idPatient.__str__()


class ConsultationType(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)


class MedicalFolder(models.Model):
    createTime = models.TimeField(auto_now=True)
    createDate = models.DateField(auto_now=True)
    lastModificationTime = models.TimeField(auto_now=True)
    lastModificationDate = models.DateField(auto_now=True)
    folderCode = models.CharField(max_length=300)
    isClosed = models.BooleanField()

    idActualParam = models.ForeignKey("Parameters", on_delete=models.CASCADE, null=True)


class MedicalFolderPage(models.Model):
    pageNumber = models.IntegerField()
    addTime = models.TimeField(auto_now=True)
    addDate = models.DateField(auto_now=True)
    remark = models.TextField(max_length=10000, blank=True, null=True)

    idMedicalFolder = models.ForeignKey("MedicalFolder", on_delete=models.CASCADE, null=True)


# ======================================
# ======================================== EXAM
# ======================================


class Exam(models.Model):
    examName = models.CharField(max_length=100)
    examCost = models.FloatField()
    examDescription = models.TextField(max_length=23, blank=True, null=True)


class ExamRequest(models.Model):
    addTime = models.TimeField(auto_now=True)
    addDate = models.DateField(auto_now=True)
    examDetails = models.CharField(max_length=50, null=True)
    examStatus = models.CharField(max_length=20, default="invalid")
    patientStatus = models.CharField(max_length=20, default="invalid")
    notes = models.TextField(max_length=10000, blank=True, null=True)

    idExam = models.ForeignKey("Exam", on_delete=models.CASCADE, null=False)
    idMedicalFolderPage = models.ForeignKey("MedicalFolderPage", on_delete=models.CASCADE, null=False)
    idPatient = models.ForeignKey("Patient", on_delete=models.CASCADE, null=False)
    idMedicalStaff = models.ForeignKey("MedicalStaff", on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.idPatient) + ' ' + str(self.ExamDescription)


class ExamResult(models.Model):
    addTime = models.TimeField(auto_now=True)
    addDate = models.DateField(auto_now=True)
    notes = models.TextField(max_length=10000, blank=True, null=True)

    idExamRequest = models.ForeignKey("ExamRequest", on_delete=models.CASCADE, null=False)
    idMedicalFolderPage = models.ForeignKey("MedicalFolderPage", on_delete=models.CASCADE, null=False)
    idPatient = models.ForeignKey("Patient", on_delete=models.CASCADE, null=False)
    idMedicalStaff = models.ForeignKey("MedicalStaff", on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.idPatient) + ' ' + str(self.ExamDescription)


# ======================================
# ======================================== MEDICAMENT, PRESCRIPTION, ROOM, HOSPITALISATION
# ======================================


class Medicament(models.Model):
    addTime = models.TimeField(auto_now=True)
    addDate = models.DateField(auto_now=True)
    quantity = models.IntegerField()
    medicamentName = models.CharField(max_length=50, null=False, default="")
    status = models.CharField(max_length=20, default="invalid")
    medicamentCost = models.FloatField(max_length=20, null=False, default="0.0")
    expiryDate = models.DateField(auto_now=False)
    description = models.TextField(max_length=200, null=False, default="important")

    def __str__(self):
        return self.medicamentName.__str__() + " " + self.quantity.__str__()


class Prescription(models.Model):
    addTime = models.TimeField(auto_now=True)
    addDate = models.DateField(auto_now=True)
    dose = models.TextField()

    idPatient = models.ForeignKey("Patient", on_delete=models.CASCADE, null=False)
    idMedicalFolderPage = models.ForeignKey("MedicalFolderPage", on_delete=models.CASCADE, null=False)
    idMedicalStaff = models.ForeignKey("MedicalStaff", on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.dose.__str__() + " " + self.idPatient.__str__()


class Room(models.Model):
    roomLabel = models.CharField(max_length=100)
    beds = models.PositiveIntegerField(default = 0)
    busyBeds = models.IntegerField(default = 0)


class Hospitalisation(models.Model):
    atDate = models.DateField(auto_now=True)
    atTime = models.TimeField(auto_now=True)
    bedLabel = models.CharField(max_length=100)
    note = models.TextField()
    isActive = models.BooleanField(default=True)
    removeAt = models.DateTimeField(auto_now=True)

    idRoom = models.ForeignKey("Room", on_delete=models.CASCADE, null=False)
    idPatient = models.ForeignKey("Patient", on_delete=models.CASCADE, null=False)
    idMedicalStaff = models.ForeignKey("MedicalStaff", on_delete=models.CASCADE, null=False)


# La classe pour la facture
class Bill(models.Model):
    customer = models.CharField(max_length=50)
    tel = models.CharField(max_length=20, default="0")
    date = models.DateTimeField(auto_now=True)
    amount = models.FloatField(default=0.0)
    totalItems = models.IntegerField(default=0)


class BillItem(models.Model):
    idBill = models.ForeignKey("Bill", on_delete=models.CASCADE, null=False)
    idMedicament = models.ForeignKey("Medicament", on_delete=CASCADE, null=False)
    quantity = models.PositiveIntegerField(default=0)
    designation = models.CharField(max_length=50)
    unitP = models.FloatField(default=0.0)
    totalP = models.FloatField(default=0.0)


# ======================================
# ======================================== I DON'T NO
# ======================================
#
# class Drog(models.Model):
#     medecineName = models.CharField(max_length=100)
#     medecineCoast = models.FloatField()


class Message(models.Model):
    addAt = models.DateTimeField(auto_now=True)
    message = models.TextField()
    reason = models.TextField()
    messageType = models.CharField(max_length=30, choices=MessageType, default='INFO')

    idMedicalStaff = models.ForeignKey("MedicalStaff", on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.dose.__str__() + " " + self.idPatient.__str__()
