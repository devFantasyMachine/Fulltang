from django.urls import path, include
from polyclinic.views.reception import index, add_patient, details_patients


urlpatterns = [

    path('<str:username>', index),
    path('patients/add', add_patient),
    path('patients/details/<int:id>', details_patients),



]


def reception_urls():
    return urlpatterns, 'reception', 'reception'

