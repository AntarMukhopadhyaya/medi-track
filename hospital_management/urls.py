"""
URL configuration for hospital_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("appointments/", views.get_appointments, name="patient_appointments"),
    path("cancel_appointment/<int:appointment_id>",
         views.cancel_appointment, name="cancel_patient_appointments"),
    path("prescriptions/", views.get_prescriptions, name="patient_prescriptions"),
    path("show_prescription/<int:id>",
         views.show_prescription, name="show_prescription"),
    path("search/", views.search_results, name="search"),
    path("hospital/", include("hospital.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
