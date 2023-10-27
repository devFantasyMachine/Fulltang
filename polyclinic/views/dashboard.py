import sqlite3

import django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from polyclinic.forms import StaffForm
from polyclinic.models import MedicalStaff, ConsultationType,Exam,Room,Patient
from django.db.models import Count

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

roles =['NoRole', "Admin",'Doctor','Receptionist','Accountant','Nurse','Labtech','Specialist','Ophtalmologist','Pharmacist','Dentist','Cashier']


#@login_required(login_url='/')
def index(request):
    staffs = MedicalStaff.objects.values('role').annotate(numbers = Count('id'))
    patients = Patient.objects.count()
    return render(request,'dashboard/index.html',{'list':staffs,'roles':roles,'patients':patients})


#@login_required(login_url='/')
def get_add_staff(request): 
    # this method summon the html page in order to register a staff

    if request.user.role == "Admin":
        context = {"roles": roles}
        return render(request,'dashboard/staff_registration.html',context)

    #return redirect("/")

#@login_required(login_url='/')
def add_staff(request):
    # when the form is submitted, this is the hanled method in which a new instance of a medical staff is saved

    if request.method == 'POST':

        username = request.POST['username']

        try:

            MedicalStaff.objects.create_user(username=username,
                                        email=request.POST ['email'],
                                        password=request.POST['password'],
                                        first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        gender=request.POST['gender'],
                                        cniNumber=request.POST['cniNumber'],
                                        role=request.POST['role'],
                                        )

            staffs = MedicalStaff.objects.all()

            paginator = Paginator(staffs, 7)
            staff_lists = paginator.get_page(paginator.num_pages)

            return render(request, 'dashboard/staff_list.html', {'staff_list': staff_lists})

        except (sqlite3.IntegrityError, django.db.utils.IntegrityError) as error:

            context = {"roles": roles, "username" : username, "with_error" : True }
            return render(request, 'dashboard/staff_registration.html', context)

    return redirect('/dashboard/get_staff_registration')


@login_required(login_url='/')
def edit (request,id):
    
    # this method summon the html page in order to update informations of a staff
    # in the link associated to the "a" tag of the template, we pass the id of each staff
    # and we return the corrsponding one to the template so that it previous informationc can be loaded

    staff = MedicalStaff.objects.get(id = id)
    return render(request,'dashboard/staff_update.html',{"mS":staff,'roles':roles})


@login_required(login_url='/')
def update(request,id):
    
    medicalStaff = MedicalStaff.objects.get(id = id)
    medicalStaff.username=request.POST['username']
    medicalStaff.first_name = request.POST['first_name']
    medicalStaff.last_name = request.POST['last_name']
    medicalStaff.gender = request.POST['gender']
    medicalStaff.cniNumber = request.POST['cniNumber']
    medicalStaff.role = request.POST['role']
    medicalStaff.email = request.POST ['email']
    medicalStaff.save()
    return redirect('/dashboard/staff_list') 


@login_required(login_url='/')
def remove (request,id):
        ms = MedicalStaff.objects.get(id=id)
        ms.delete()
       
        return redirect('/dashboard/staff_list') 

#@login_required(login_url='/')
def staff_list (request):
    staffs = MedicalStaff.objects.all()
    paginator = Paginator(staffs, 7)
    page = request.GET.get('page')
    staff_lists = paginator.get_page(page)
    name = ''
    
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            ms = MedicalStaff.objects.filter(username__contains = name)
            paginator = Paginator(ms, 7)
            page = request.GET.get('page')
            staff_lists = paginator.get_page(page)
            

    return render(request, 'dashboard/staff_list.html', {'staff_list': staff_lists,'select_name' : name})

@login_required(login_url='/')
def get_add_consultation (request):
    return render(request,'dashboard/consultation.html')   

@login_required(login_url='/')
def add_consultation (request):
    ConsultationType.objects.create(name = request.POST["name"],
                                    price = request.POST["price"])
        
    return redirect('/dashboard/consultation_list')

@login_required(login_url='/')
def consultation_list(request):
    list = ConsultationType.objects.all()
    return render(request,'dashboard/consultation_list.html',{'list':list})

#....................................
#....................Exam............

@login_required(login_url='/')
def get_add_exam (request):
    return render(request,'dashboard/exam.html')   

@login_required(login_url='/')
def add_exam (request):
    Exam.objects.create(examName = request.POST["examName"],
                        examCost = request.POST["examCost"],
                        examDescription = request.POST["examDescription"])
                        
        
    return redirect('/dashboard/exam_list')

@login_required(login_url='/')
def exam_list(request):
    list = Exam.objects.all()
    return render(request,'dashboard/exam_list.html',{'list':list})

def get_add_room(request):
    return render(request,'dashboard/room.html')

def add_room(request):
    Room.objects.create(roomLabel = request.POST["roomLabel"],
                        beds = request.POST["beds"])
    return redirect('/dashboard/room_list')
def room_list(request):
    list = Room.objects.all()
    paginator = Paginator(list, 7)
    page = request.GET.get('page')
    list = paginator.get_page(page)
    name = ''
    
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            ms = MedicalStaff.objects.filter(roomLabel__contains = name)
            paginator = Paginator(ms, 7)
            page = request.GET.get('page')
            list = paginator.get_page(page)
            

    return render(request, 'dashboard/room_list.html', {'list': list,'select_name' : name})
