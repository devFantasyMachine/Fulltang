from django.contrib import admin
from django.urls import path, include
from polyclinic.views.cashier import index,consultation_list,paid,validate,paid_exam
from polyclinic.views.cashier import unpaid_exam,validate_exam,exam_list,display, display_exam
urlpatterns = [

    path('', index),
    path('consultation_list', consultation_list),
    path('paid_consultation', paid),
    path('validate/<int:id>', validate),
    path('display/<int:id>', display),
    path('exam_list', exam_list),
    path('paid_exam', paid_exam),
    path('unpaid_exam', unpaid_exam),
    path('validate_exam/<int:id>', validate_exam),
    path('display_exam/<int:id>', display_exam),



]


def cashier_urls():
    return urlpatterns, 'cashier', 'cashier'
