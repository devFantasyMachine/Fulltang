from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from polyclinic.models import Consultation, Patient, Parameters, ConsultationType, MedicalStaff, ExamRequest, Exam


@csrf_exempt
def index(request):
    return render(request, 'cashier/index.html')

def consultation_list(request):
    list = Consultation.objects.all()
    paginator = Paginator(list,9)
    page = request.GET.get('page')
    list = paginator.get_page(page)
    name = ''
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            list = Consultation.objects.filter(consultationReason__contains = name)
            paginator = Paginator(list, 9)
            page = request.GET.get('page')
            list = paginator.get_page(page)
    return render (request, 'cashier/consultation_list.html',{"list":list,'select_name' : name })

def exam_list(request):
    list = ExamRequest.objects.all()
    paginator = Paginator(list,9)
    page = request.GET.get('page')
    list = paginator.get_page(page)
    name = ''
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            list = ExamRequest.objects.filter(idExam__contains = name)
            paginator = Paginator(list, 9)
            page = request.GET.get('page')
            list = paginator.get_page(page)
    return render (request, 'cashier/exam_list.html',{"list":list,'select_name' : name })

def unpaid(request):
    list = Consultation.objects.filter(status = 'invalid')
    paginator = Paginator(list,9)
    page = request.GET.get('page')
    list = paginator.get_page(page)
    name = ''
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            list = Consultation.objects.filter(consultationReason__contains = name)
            paginator = Paginator(list, 9)
            page = request.GET.get('page')
            list = paginator.get_page(page)
    return render (request, 'cashier/unpaid_exam.html',{"list":list,'select_name' : name })

def unpaid_exam(request):
    list = ExamRequest.objects.filter(examStatus = 'invalid')
    paginator = Paginator(list,9)
    page = request.GET.get('page')
    list = paginator.get_page(page)
    name = ''
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            list = ExamRequest.objects.filter(examName__contains = name)
            paginator = Paginator(list, 9)
            page = request.GET.get('page')
            list = paginator.get_page(page)
    return render (request, 'cashier/unpaid_exam.html',{"list":list,'select_name' : name })


def validate(request,id):
    consultation = Consultation.objects.get(id =id )
    consultation.status = 'valid'
    consultation.save()
    return redirect('/cashier/consultation_list')

def validate_exam(request,id):
    exam = ExamRequest.objects.get(id =id )
    exam.status = 'valid'
    exam.save()
    return redirect('/cashier/exam_list')

def paid(request):
    list = Consultation.objects.filter(status = 'valid')
    paginator = Paginator(list,9)
    page = request.GET.get('page')
    list = paginator.get_page(page)
    name = ''
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            list = Consultation.objects.filter(consultationReason__contains = name)
            paginator = Paginator(list, 9)
            page = request.GET.get('page')
            list = paginator.get_page(page)
    return render (request, 'cashier/paid_consultation.html',{"list":list,'select_name' : name })

def paid_exam(request):
    list = ExamRequest.objects.filter(examStatus = 'valid')
    paginator = Paginator(list,9)
    page = request.GET.get('page')
    list = paginator.get_page(page)
    name = ''
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            list = ExamRequest.objects.filter(examName__contains = name)
            paginator = Paginator(list, 9)
            page = request.GET.get('page')
            list = paginator.get_page(page)
    return render (request, 'cashier/paid_exam.html',{"list":list,'select_name' : name })


def display(request,id):
    consultation = Consultation.objects.get(id=id)
    patient = Patient.objects.get(id = consultation.idPatient)
    param = Parameters.objects.get(id = consultation.idParameters)
    type = ConsultationType.objects.get(id = consultation.idConsultationType)
    staff= MedicalStaff.objects.get(id = consultation.idMedicalStaff)
    return render(request, 'cashier/display.html', {'consultation': consultation,'patient':patient,
                                                    'param':param,'type':type,'staff':staff})

def display_exam(request,id):
    examRequest = ExamRequest.objects.get(id=id)
    patient = Patient.objects.get(id= examRequest.idPatient)
    staff= MedicalStaff.objects.get(id = examRequest.idMedicalStaff)
    exam = Exam.objects.get(id = examRequest.id)

    return render(request, 'cashier/display.html', {'exam': exam,'patient':patient,'staff':staff,'examRequest':examRequest})


