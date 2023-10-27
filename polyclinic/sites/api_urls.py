from django.urls import path, include
from polyclinic.views.api import get_all_patients, toggleCondition, addParam, \
    details_patients, get_all_messages, addAccess, addHospitalisation, addAppointment, addMessage, addExamRequest, \
    addPrescription, removeAccess, addConsultation, removeHospitalisation

urlpatterns = [

    path('patients', get_all_patients),
    path('messages', get_all_messages),
    path('patients/add-access', addAccess),
    path('patients/remove-access/<int:id>', removeAccess),
    path('patients/add-appointment', addAppointment),
    path('patients/add-consultation', addConsultation),
    path('patients/add-hospitalisation', addHospitalisation),
    path('patients/add-param', addParam),
    path('patients/add-message', addMessage),
    path('patients/add-prescription', addPrescription),
    path('patients/add-exam-request', addExamRequest),
    path('patients/details/<int:id>', details_patients),
    path('patients/toggle-condition/<int:id>', toggleCondition),
    path('patients/remove-hospitalisation/<int:id>', removeHospitalisation),

]


def api_urls():
    return urlpatterns, 'api', 'api'
