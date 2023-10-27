from django.contrib import admin
from django.urls import path, include
from polyclinic.views.dashboard import edit,add_consultation,consultation_list,add_exam
from polyclinic.views.dashboard import add_staff, get_add_consultation,get_add_exam,exam_list
from polyclinic.views.dashboard import index,get_add_room,room_list,add_room
from polyclinic.views.dashboard import staff_list,get_add_staff,remove, update

urlpatterns = [

    path('', index),
    path('add_staff',add_staff),
    path('staff_list',staff_list),
    path('get_staff_registration',get_add_staff),
    path('delete/<int:id>',remove),
    path('update/<int:id>',update),
    path('edit/<int:id>',edit),
    path('get_add_consultation',get_add_consultation),
    path('add_consultation',add_consultation),
    path('consultation_list',consultation_list),
    path('get_add_exam',get_add_exam),
    path('add_exam',add_exam),
    path('exam_list',exam_list), 
    path('get_add_room',get_add_room),
    path('add_room',add_room),
    path('room_list',room_list)


]


def dashboard_urls():
    return urlpatterns, 'dashboard', 'dashboard'
