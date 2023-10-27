"""fultang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from polyclinic.sites.cashier_urls import cashier_urls

from polyclinic.sites.cashier_urls import cashier_urls
from polyclinic.sites.welcom_urls import welcome_urls
from polyclinic.sites.dashboard_urls import dashboard_urls
from polyclinic.sites.pharmacist_urls import pharmacist_urls
from polyclinic.sites.doctor_urls import doctor_urls
from polyclinic.sites.reception_urls import reception_urls
from polyclinic.sites.laboratory_urls import laboratory_urls
from polyclinic.sites.nurse_urls import   nurse_urls
from polyclinic.sites.api_urls import api_urls

urlpatterns = [

    path('', welcome_urls()),
    path('api/', api_urls()),

    path('dashboard/', dashboard_urls()),
    path('pharmacist/',pharmacist_urls()),
    path('doctor/', doctor_urls()),
    path('reception/', reception_urls()),
    path('nurse/', nurse_urls()),
    path('laboratory/', laboratory_urls()),
    path('admin/', admin.site.urls),
    path('cashier/', cashier_urls())

]
