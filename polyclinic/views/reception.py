from django.contrib.auth import logout
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render

from polyclinic.models import MedicalStaff, Patient, MedicalFolder, PatientAccess, Appointment, Parameters, \
    Prescription, ConsultationType, ExamRequest, Exam, ExamResult, Room, Consultation, Hospitalisation

roles = ['NoRole', 'Doctor', 'Receptionist', 'Accountant', 'Nurse', 'Labtech', 'Specialist', 'Ophtalmologist',
         'Pharmacist', 'Dentist']


@login_required(login_url='/')
def index(request, username):
    staffs = MedicalStaff.objects.all()
    appointments = Appointment.objects.all()
    hospitalisations = Hospitalisation.objects.all()
    patients = Patient.objects.all()
    rooms = Room.objects.all()

    room_stat = Room.objects.values('beds', 'busyBeds').aggregate(total_beds=Sum('beds'),
                                                                 total_busybeds=Sum('busyBeds'))

    percent = (100 * room_stat["total_busybeds"] )// room_stat["total_beds"]
    room_stat["percent"] = percent
    stat = {"patients": len(patients), 'appointments': len(appointments)}

    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            staffs = MedicalStaff.objects.filter(username__contains=name)

    return render(request, 'reception/index.html',
                  {'staff_list': staffs, "rooms":rooms, "hospitalisations": hospitalisations, "stat": stat, "room_stat": room_stat,
                   'appointments': appointments, 'roles': roles})


def logout_view(request):
    logout(request)
    # Redirect to a success page.


@login_required(login_url='/')
def details_patients(request, id):
    patient = Patient.objects.get(id=id)
    folder = MedicalFolder.objects.get(id=patient.idMedicalFolder.pk)
    parameters = None
    rooms = Room.objects.all()
    prescriptions = Prescription.objects.filter(idPatient=patient.pk)
    consultations = Consultation.objects.filter(idPatient=patient.pk)
    consultationsTypes = ConsultationType.objects.all()
    hospitalisations = Hospitalisation.objects.filter(idPatient=patient.pk)


    try:

        current_hosp = Hospitalisation.objects.get(idPatient=patient.pk, isActive=True)

    except:

        current_hosp = None

    staffs = MedicalStaff.objects.all()

    exams = Exam.objects.all()
    examRequest = ExamRequest.objects.filter(idPatient=patient.pk)
    examsResult = ExamResult.objects.filter(idPatient=patient.pk)

    if folder.idActualParam is not None:
        parameters = Parameters.objects.get(id=folder.idActualParam.pk)

    if request.user.role == "Receptionist" or request.user.role == "Admin":

        all_access = PatientAccess.objects.filter(idPatient=patient.pk, access=True)
        appointments = Appointment.objects.filter(idPatient=patient.pk)

        context = {"patient": patient, "exams": exams, "rooms": rooms, "examRequest": examRequest,
                   "examsResult": examsResult,
                   "consultationsTypes": consultationsTypes, "prescriptions": prescriptions, "parameters": parameters,
                   "all_access": all_access, 'staffs': staffs,
                   'appointments': appointments, "current_hosp": current_hosp, "consultations": consultations,
                   "hospitalisations": hospitalisations, }

        return render(request, 'reception/patient.html', context)

    elif request.user.role == "Doctor" or request.user.role == "Nurse":

        access = PatientAccess.objects.filter(access=True, idMedicalStaff=request.user, idPatient=patient)

        if access is None:
            return render(request, 'welcome/no_role.html')

        appointments = Appointment.objects.filter(idMedicalStaff=request.user.pk, idPatient=patient.pk)

        context = {"patient": patient, "exams": exams, "rooms": rooms, "examRequest": examRequest,
                   "examsResult": examsResult,
                   "consultationsTypes": consultationsTypes, "prescriptions": prescriptions, "parameters": parameters,
                   'staffs': staffs, "current_hosp": current_hosp, "consultations": consultations,
                   "hospitalisations": hospitalisations, 'appointments': appointments}

        return render(request, 'reception/patient.html', context)

    else:
        return render(request, 'welcome/no_role.html')


@login_required(login_url='/')
def add_patient(request):
    if request.method == 'POST':

        if request.user.role == "Receptionist" or request.user.role == "Admin":
            cniNumber = request.POST['cniNumber']
            gender = request.POST['gender']
            print(cniNumber)

            mfolder = MedicalFolder(folderCode=gender + cniNumber, isClosed=False)
            mfolder.save()

            patient = Patient(idMedicalFolder=mfolder,
                              cniNumber=request.POST['cniNumber'],
                              firstName=request.POST['firstName'],
                              lastName=request.POST['lastName'],
                              gender=request.POST['gender'],
                              phoneNumber=request.POST['phoneNumber'],
                              birthDate=request.POST['birthDate'],
                              address=request.POST['address'],
                              email=request.POST['email'],
                              condition=request.POST['condition'], )

            patient.save()

            return JsonResponse({"patient_id": patient.pk})

    else:
        return render(request, 'welcome/no_role.html')
