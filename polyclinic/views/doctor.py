from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from polyclinic.models import Appointment, MedicalStaff, PatientAccess, ExamResult, ExamRequest, Exam

roles =['NoRole','Doctor','Receptionist','Accountant','Nurse','Labtech','Specialist','Ophtalmologist','Pharmacist','Dentist']


def index(request, username):


    if request.user.role == "Doctor" :

        patients = []
        medicalStaff = MedicalStaff.objects.get(id=request.user.pk)

        all_access = PatientAccess.objects.filter(access=True, idMedicalStaff=medicalStaff)

        for access in all_access:
            patients.append(access.idPatient)

        examsResult = []
        examRequest = ExamRequest.objects.filter(idMedicalStaff=request.user.pk)
        for r in examRequest :
            examsResult.append(ExamResult.objects.get(idExamRequest=r.pk))

        appointments = Appointment.objects.filter(idMedicalStaff=request.user.pk)
        exams = Exam.objects.all()
        staffs = MedicalStaff.objects.all()
        stat = {"patients" : len(patients)  , 'appointments' : len(appointments)}

        context = {"patients" : patients, 'staffs' : staffs, 'exams': exams, 'stat' : stat, 'examRequest': examRequest, 'examsResult':examsResult, 'appointments' : appointments, 'roles' : roles}

        return render(request, 'doctor/index.html', context)
    else :
        return redirect("/")
