from django.contrib.auth import authenticate, logout, login as signin
from django.core.serializers import serialize
from django.db.models.functions import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from polyclinic.models import MedicalStaff, Patient, Message, MedicalFolder, PatientAccess, Appointment, Parameters, \
    MessageType, Prescription, MedicalFolderPage, Consultation, ConsultationType, Exam, ExamRequest, ExamResult, \
    Hospitalisation, Room
from polyclinic.views.doctor import index as doctor_index
from polyclinic.views.pharmacist import index as pharmacist_index

roles = ['NoRole', 'Doctor', 'Receptionist', 'Accountant', 'Nurse', 'Labtech', 'Specialist', 'Ophtalmologist',
         'Pharmacist', 'Dentist']


@login_required(login_url='/')
def index(request):
    staffs = MedicalStaff.objects.all()

    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            staffs = MedicalStaff.objects.filter(username__contains=name)

    return render(request, 'reception/index.html', {'staff_list': staffs, 'roles': roles})


def logout_view(request):
    logout(request)
    # Redirect to a success page.


@login_required(login_url='/')
def details_patients(request, id):
    if request.user.role == "Receptionist" or request.user.role == "Admin":

        patient = Patient.objects.get(id=id)

        print("patient " + str(patient))

        context = {"patient": patient}

        return render(request, 'reception/patient.html', context)


    else:
        return render(request, 'welcome/no_role.html')


@login_required(login_url='/')
def get_all_patients(request):
    if request.user.role == "Receptionist" or request.user.role == "Admin":

        patients = Patient.objects.all()

        data = serialize("json", patients)
        return JsonResponse(data, content_type="application/json", safe=False)

    else:

        patients = []

        medicalStaff = MedicalStaff.objects.get(id=request.user.pk)

        all_access = PatientAccess.objects.filter(access=True, idMedicalStaff=medicalStaff)

        for access in all_access:
            patients.append(access.idPatient)

        data = serialize("json", patients)
        return JsonResponse(data, content_type="application/json", safe=False)

    return HttpResponse(status=403)


@login_required(login_url='/')
def get_all_messages(request):
    if request.user.role == "Receptionist" or request.user.role == "Admin":
        messages = Message.objects.all()

        data = serialize("json", messages)

        return JsonResponse(data, content_type="application/json", safe=False)

    return HttpResponse(status=403)


@login_required(login_url='/')
def addAccess(request):
    if request.user.role == "Receptionist" or request.user.role == "Admin":

        patient = Patient.objects.get(id=request.POST['idPatient'])
        medicalStaff = MedicalStaff.objects.get(id=request.POST['idMedicalStaff'])

        p = PatientAccess.objects.filter(access=True, idPatient=patient, idMedicalStaff=medicalStaff).count()
        print(p)

        if p is None or p == 0:

            access = PatientAccess(access=True, idPatient=patient, idMedicalStaff=medicalStaff)
            access.save()

            return HttpResponse(status=200)

        else:

            return HttpResponse(status=200)

    return HttpResponse(status=403)


@login_required(login_url='/')
def removeAccess(request, id):

    if request.user.role == "Receptionist" or request.user.role == "Admin":

        p = PatientAccess.objects.get(id=id)
        p.access = False
        p.lostAt = datetime.timezone.now()
        p.save()

        return HttpResponse(status=200)

    return HttpResponse(status=403)



@login_required(login_url='/')
def addAppointment(request):
    if request.user.role == "Doctor" or request.user.role == "Admin":
        patient = Patient.objects.get(id=request.POST['idPatient'])
        medicalStaff = MedicalStaff.objects.get(id=request.user.pk)

        appointment = Appointment(atDate=request.POST['atDate'], reason=request.POST['reason'],
                                  requirements=request.POST['requirements'], idPatient=patient,
                                  idMedicalStaff=medicalStaff)
        appointment.save()

        return HttpResponse(status=200)

    return HttpResponse(status=403)


@login_required(login_url='/')
def addParam(request):
    if request.user.role == "Doctor" or request.user.role == "Nurse":
        patient = Patient.objects.get(id=request.POST['idPatient'])
        medicalStaff = MedicalStaff.objects.get(id=request.user.pk)
        folder = MedicalFolder.objects.get(id=patient.idMedicalFolder.pk)

        params = Parameters(weight=request.POST['weight'], height=request.POST['height'],
                            temperature=request.POST['temperature'], arterialPressure=request.POST['arterialPressure'],
                            skinAppearance=request.POST['skinAppearance'],
                            idMedicalFolder=patient.idMedicalFolder, idMedicalStaff=medicalStaff)

        params.save()
        folder.idActualParam = params
        folder.save()
        print(folder.idActualParam)


        return HttpResponse(status=200)

    return HttpResponse(status=403)


@login_required(login_url='/')
def addMessage(request):

    medicalStaff = MedicalStaff.objects.get(id=request.user.pk)
    message = Message(message=request.POST['message'], reason=request.POST['reason'], messageType="Info", idMedicalStaff=medicalStaff)

    message.save()

    return HttpResponse(status=200)




@login_required(login_url='/')
def toggleCondition(request, id):
    if request.user.role == "Doctor" or request.user.role == "Receptionist":
        patient = Patient.objects.get(id=id)

        if patient.condition == "Critical" :
            patient.condition = "NoCritical"
        else :
            patient.condition = "Critical"

        patient.save()

        return HttpResponse(status=200)

    return HttpResponse(status=403)



@login_required(login_url='/')
def addPrescription(request):
    if request.user.role == "Doctor":
        patient = Patient.objects.get(id=request.POST['idPatient'])
        medicalStaff = MedicalStaff.objects.get(id=request.user.pk)
        folder = MedicalFolder.objects.get(id=patient.idMedicalFolder.pk)
        page_count = MedicalFolderPage.objects.filter(idMedicalFolder=folder)

        page = MedicalFolderPage(pageNumber=len(page_count), idMedicalFolder=folder, remark="Prescription")
        page.save()

        prescription = Prescription(dose=request.POST['dose'], idPatient=patient, idMedicalFolderPage=page,
                                  idMedicalStaff=medicalStaff)

        prescription.save()

        return HttpResponse(status=200)

    return HttpResponse(status=403)


@login_required(login_url='/')
def addConsultation(request):
    if request.user.role == "Doctor":
        patient = Patient.objects.get(id=request.POST['idPatient'])
        medicalStaff = MedicalStaff.objects.get(id=request.user.pk)
        folder = MedicalFolder.objects.get(id=patient.idMedicalFolder.pk)
        page_count = MedicalFolderPage.objects.filter(idMedicalFolder=folder)
        parameters = Parameters.objects.get(id=folder.idActualParam.pk)

        page = MedicalFolderPage(pageNumber=len(page_count), idMedicalFolder=folder, remark="Consultation")
        page.save()

        consultationType = ConsultationType.objects.get(id= request.POST['type'])


        consultation = Consultation(consultationNotes=request.POST['consultationNotes'],
                                    consultationReason=request.POST['consultationReason'],
                                    allergy=request.POST['allergy'],
                                    previousHistory=request.POST['previousHistory'],
                                    status=request.POST['status'],
                                    consultationCost=consultationType.price,
                                    idConsultationType= consultationType,
                                    idParameters=parameters,
                                    idPatient=patient,
                                    idMedicalFolderPage=page,
                                    idMedicalStaff=medicalStaff)


        consultation.save()

        return HttpResponse(status=200)

    return HttpResponse(status=403)




@login_required(login_url='/')
def addExamRequest(request):
    if request.user.role == "Doctor":
        patient = Patient.objects.get(id=request.POST['idPatient'])
        medicalStaff = MedicalStaff.objects.get(id=request.user.pk)
        folder = MedicalFolder.objects.get(id=patient.idMedicalFolder.pk)
        page_count = MedicalFolderPage.objects.filter(idMedicalFolder=folder)


        page = MedicalFolderPage(pageNumber=len(page_count), idMedicalFolder=folder, remark="Consultation")
        page.save()


        exam = Exam.objects.get(id= request.POST['exam'])


        examRequest = ExamRequest(notes=request.POST['notes'],
                                    examDetails=request.POST['examDetails'],
                                    idExam= exam,
                                    idPatient=patient,
                                    idMedicalFolderPage=page,
                                    idMedicalStaff=medicalStaff)



        examRequest.save()

        return HttpResponse(status=200)

    return HttpResponse(status=403)


@login_required(login_url='/')
def addHospitalisation(request):
    if request.user.role == "Receptionist":
        patient = Patient.objects.get(id=request.POST['idPatient'])
        medicalStaff = MedicalStaff.objects.get(id=request.user.pk)

        room = Room.objects.get(id= request.POST['room'])

        if room.busyBeds == room.beds :
            return HttpResponse(status=403)

        hospitalisation = Hospitalisation(note=request.POST['note'],
                                    bedLabel=request.POST['bedLabel'],
                                    isActive = True,
                                    idRoom= room,
                                    idPatient=patient,
                                    idMedicalStaff=medicalStaff)

        hospitalisation.save()

        room.busyBeds = room.busyBeds + 1
        room.save()

        return HttpResponse(status=200)

    return HttpResponse(status=401)



@login_required(login_url='/')
def removeHospitalisation(request, id):

    if request.user.role == "Receptionist" or request.user.role == "Admin":

        p = Hospitalisation.objects.get(id=id)
        p.removeAt = datetime.timezone.now()
        p.isActive = False
        p.save()

        room = Room.objects.get(id=request.POST['room'])

        room.busyBeds = room.busyBeds - 1
        room.save()

        return HttpResponse(status=200)

    return HttpResponse(status=401)








