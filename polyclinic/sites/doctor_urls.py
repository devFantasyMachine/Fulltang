from django.contrib import admin
from django.urls import path, include
from polyclinic.views.doctor import index

urlpatterns = [

    path('<str:username>', index),
    #path('<str:username>/patients/add-param/<int:id>', add_param),
    #path('<str:username>/patients/details/<int:id>', details_patients),

]


def doctor_urls():
    return urlpatterns, 'doctor', 'doctor'
