from django.urls import path, include
from polyclinic.views.laboratory import index, examlist, examhistory, examresult, saveExamResult

urlpatterns = [

    path('', index),
    path('home', index),
    path('examlist', examlist),
    path('examresult/<int:id>', examresult),
    path('examresult/saveExamResult/<int:id>', saveExamResult),
    path('examhistory', examhistory),

]


def laboratory_urls():
    return urlpatterns, 'laboratory', 'laboratory'
