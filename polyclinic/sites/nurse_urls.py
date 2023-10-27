from django.urls import path, include
from polyclinic.views.nurse import index, add_param, details_patients


urlpatterns = [

    path('<str:username>', index),
    path('<str:username>/patients/add-param/<int:id>', add_param),
    path('<str:username>/patients/details/<int:id>', details_patients),



]


def nurse_urls():
    return urlpatterns, 'nurse', 'nurse'

