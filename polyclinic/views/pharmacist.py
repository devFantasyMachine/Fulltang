from django.shortcuts import render, redirect
from polyclinic.models import Medicament, Bill, BillItem
from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404


@csrf_exempt
def index(request, username):
    return render(request, 'pharmacist/index.html')

def get_add_medicament(request):
    return render(request,'pharmacist/add_medicament.html')

def add_medicament(request):
    Medicament.objects.create(quantity = request.POST['quantity'],
                              medicamentName = request.POST['name'],
                              status = request.POST['status'],
                              medicamentCost = request.POST['cost'],
                              expiryDate = request.POST['expiry'],
                              description = request.POST['description'] 
                              )
    return redirect('/pharmacist/get_add_medicament')

def edit (request,id):
    medicament = Medicament.objects.get(id=id)
    return render(request,'pharmacist/medicament_update.html',{'medicament':medicament})

def update (request, id):
    medicament = Medicament.objects.get(id = id)
    medicament.quantity = request.POST['quantity']
    medicament.medicamentName = request.POST['name']
    medicament.status = request.POST['status']
    medicament.description = request.POST['description']
    medicament.expiryDate = request.POST['expiry']
    medicament.medicamentCost = request.POST['cost']
    medicament.save()

    return redirect('/pharmacist/medicament_list')

def remove (request,id):
    medicament = Medicament.objects.get(id=id)
    medicament.delete()
       
    return redirect('/pharmacist/medicament_list') 

def medicament_list(request):
    list = Medicament.objects.all()
    paginator = Paginator(list,7)
    page = request.GET.get('page')
    list = paginator.get_page(page)
    name = ''
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            list = Medicament.objects.filter(medicamentName__contains = name)
            paginator = Paginator(list, 7)
            page = request.GET.get('page')
            list = paginator.get_page(page)
    return render (request, 'pharmacist/medicament_list.html',{"list":list,'select_name' : name })
    
""".....................managing bills and bills items..................."""
""".....................managing bills and bills items..................."""
""".....................managing bills and bills items..................."""
""".....................managing bills and bills items..................."""

def new_bill (request):
    # create a new bill and render the billing page
    bill = Bill.objects.create(customer = request.POST["customer"],
                               tel = request.POST["tel"])
    
    list = Medicament.objects.all()
    paginator = Paginator(list,7)
    page = request.GET.get('page')
    list = paginator.get_page(page)
    name = ''
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            list = Medicament.objects.filter(medicamentName__contains = name)
            paginator = Paginator(list, 7)
            page = request.GET.get('page')
            list = paginator.get_page(page)
    return render (request, 'pharmacist/new_bill.html',{"list":list,'select_name' : name, 'bill':bill })

def save_bill (request,id) :
    #get the current bill and save fields (totalItems and amount) computed on the client side
    bill = Bill.objects.get(id = id)
    bill.totalItems =request.POST["items"]
    bill.amount = request.POST['amount']
    bill.save()
    #getting all the bill's data
    data = request.POST["data"]
    #cleaning data and formating it in a suited form
    items = data.split('>')
    clean = [0 for i in range(len(items))]
    for i in range(len(items)):
        clean[i] = items[i].split(" ")
        clean[i].pop(0)
        clean[i].pop(5)
    #saving each billItem  extracted from the cleaned data to the corresponding bill
    for i in range(len(items)):
        med = Medicament.objects.get(id=clean[i][0])
        
        BillItem.objects.create(idBill=bill,
                                idMedicament = med,
                                designation = med.medicamentName,
                                quantity = clean[i][1],
                                unitP =clean[i][2],
                                totalP = clean[i][3] )

        med.quantity = med.quantity - int(clean[i][1])
        med.save()
        
    list = BillItem.objects.filter(idBill = id)
    bill = Bill.objects.get(id = id)
    return render(request, 'pharmacist/bill_details.html',{'list':list,'bill':bill})

def bills(request):

    bills = Bill.objects.all()
    paginator = Paginator(bills,7)
    page = request.GET.get('page')
    bills = paginator.get_page(page)
    name = ''
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
            bills = Bill.objects.filter(customer__contains = name)
            paginator = Paginator(bills, 7)
            page = request.GET.get('page')
            bills = paginator.get_page(page)
    return render (request, 'pharmacist/bills.html',{"bills":bills,'select_name' : name })

def details(request,id):
    bill = Bill.objects.get(id = id)
    list = BillItem.objects.filter(idBill=bill)
    return render (request, 'pharmacist/bill_details.html',{'list':list,"bill":bill})




