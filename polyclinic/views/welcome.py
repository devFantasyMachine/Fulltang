from django.contrib.auth import authenticate, logout, login as signin
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from polyclinic.models import MedicalStaff
from polyclinic.views.doctor import index as doctor_index
from polyclinic.views.pharmacist import index as pharmacist_index


@csrf_exempt
def index(request):
    username = ''
    password = ''
    if request.method == 'POST':
        if 'username' in request.POST:
            username = request.POST['username']
        if 'password' in request.POST:
            password = request.POST['password']

        user = authenticate(request,username=username, password=password)
        print(user)

        if user is not None:
            signin(request, user)

            return redirect("/home")

        else:

            return render(request, 'welcome/index.html', {"username" : username, "error" : True})

    return render(request, 'welcome/index.html', {})





@login_required(login_url='/')
def home(request):

    if request.user.role == "Receptionist":
        return redirect('/reception/' + request.user.username)
    elif request.user.role == "Nurse":
        return redirect("/nurse/" + request.user.username )
    elif request.user.role == "Doctor":
        return redirect("/doctor/" + request.user.username )

    elif request.user.role == "Pharmacist":
        return pharmacy(request)
    elif request.user.role == "Labtech":
        return laboratory(request)
    elif request.user.role == "Accountant":
        return reception(request)
    elif request.user.role == "Dentist":
        return dentalunit(request)


    elif request.user.role == "Admin" :
        return redirect('/dashboard')
    else:
        return render(request, 'welcome/no_role.html')


def reception(request):
    return render(request, 'reception/index.html')




def pharmacy(request):
    return render(request, 'pharmacist/index.html')


def cashdesk(request):
    return render(request, 'cashier/index.html')


def laboratory(request):
    return render(request, 'laboratory/index.html')


def dentalunit(request):
    return render(request, 'usermanagement/description/dentalunit.html')


def genMedicine(request):
    return render(request, 'usermanagement/description/genMedicine.html')


def ophtalmoservice(request):
    return render(request, 'usermanagement/description/ophtalmoservice.html')






