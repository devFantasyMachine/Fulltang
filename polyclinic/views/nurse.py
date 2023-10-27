from django.contrib.auth import authenticate, logout, login as signin
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from polyclinic.models import MedicalStaff, Patient, MedicalFolder, PatientAccess
from polyclinic.views.doctor import index as doctor_index
from polyclinic.views.pharmacist import index as pharmacist_index


roles =['NoRole','Doctor','Receptionist','Accountant','Nurse','Labtech','Specialist','Ophtalmologist','Pharmacist','Dentist']


@login_required(login_url='/')
def index(request, username):
    staffs =  MedicalStaff.objects.all()
    medicalStaff = MedicalStaff.objects.get(id=request.user.pk)

    patients = []

    all_access = PatientAccess.objects.filter(access=True, idMedicalStaff=medicalStaff)

    for access in all_access :

        patients.append(access.idPatient)


    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            staffs = MedicalStaff.objects.filter(username__contains = name)

    return render(request, 'nurse/index.html', {'staffs': staffs,'roles' : roles, 'patients' : patients})




@login_required(login_url='/')
def details_patients(request, username, id):

    if request.user.role == "Receptionist" or request.user.role == "Admin":

        patient = Patient.objects.get(id= id)

        print("patient " + str(patient))

        context = {"patient" : patient}

        return render(request, 'reception/patient.html', context)


    else:
        return render(request, 'welcome/no_role.html')


@login_required(login_url='/')
def add_param(request, username, id):

    if request.method == 'POST' :

        if request.user.role == "Receptionist" or request.user.role == "Admin":

            cniNumber = cniNumber= request.POST['cniNumber']
            gender = request.POST['gender']
            print(cniNumber)


            mfolder = MedicalFolder(folderCode = gender + cniNumber, isClosed = False)
            mfolder.save()


            patient = Patient(idMedicalFolder = mfolder,
                              cniNumber= request.POST['cniNumber'],
                              firstName=request.POST['firstName'],
                              lastName=request.POST['lastName'],
                              gender=request.POST['gender'],
                              phoneNumber=request.POST['phoneNumber'],
                              birthDate=request.POST['birthDate'],
                              address=request.POST['address'],
                              email=request.POST['email'],
                              condition=request.POST['condition'], )

            patient.save()

            return JsonResponse({"patient_id" : patient.pk})

    else:
        return render(request, 'welcome/no_role.html')





