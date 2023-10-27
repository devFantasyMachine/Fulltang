from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from polyclinic.models import ExamRequest, ExamResult, Patient, Exam, MedicalFolder, MedicalFolderPage


@csrf_exempt
@login_required(login_url='/')
def index(request):
    return render(request, 'laboratory/index.html')


# for displaying the exams which need the technician
def examlist(request):
    exams = ExamRequest.objects.filter(examStatus='invalid')

    if request.method == 'POST':
        if 'name' in request.POST:
            examName = request.POST['name']


    context = {
        'exams': exams
    }
    return render(request=request, template_name='laboratory/view_exam_list.html', context=context)


# for displaying the exams history
def examhistory(request):
    examName = ''
    if request.method == 'POST':
        if 'name' in request.POST:
            examName = request.POST['name']
    examList = ExamResult.objects.filter().order_by("addDate")[::-1]
    context = {
        'examList': examList
    }
    return render(request=request, template_name='laboratory/view_exam_history.html', context=context)


# for getting the exam results
@login_required(login_url='/')
def examresult(request, id):
    if request.method == 'POST':
        exams = ExamRequest.objects.filter(idPatient__exact=id)
        validExam = []
        cost = []
        for m in exams:
            if str(m.id) in request.POST:
                if request.POST[str(m.id)] == 'valid':
                    validExam.append(m)
                    m.status = 'valid'
                    m.save()
        patient = Patient.objects.filter(id__exact=id)[0]
        context = {
            'validExam': validExam[0],
            'patient': patient
        }
        return render(request, 'laboratory/get_exam_result.html', context=context)
    return examlist(request)


def saveExamResult(request, id):
    requestExam = ExamRequest.objects.get(id=id)
    patient = Patient.objects.get(id=requestExam.idPatient.pk)
    folder = MedicalFolder.objects.get(id=patient.idMedicalFolder.pk)
    page_count = MedicalFolderPage.objects.filter(idMedicalFolder=folder)

    page = MedicalFolderPage(pageNumber=len(page_count), idMedicalFolder=folder, remark="Resultat d'examen")
    page.save()

    result = ExamResult(notes=request.POST["notes"], idExamRequest=requestExam, idMedicalFolderPage=page, idMedicalStaff=request.user,
                        idPatient=requestExam.idPatient, )

    result.save()

   # Save the result and valid the request
    requestExam.examStatus = 'valid'
    requestExam.save()
    exam = Exam.objects.get(id=requestExam.idExam.pk)

    context = {
        'p': patient,
        'result': result,
        'ExamName': exam
    }
    return examlist(request)
