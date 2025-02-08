
from hospital.models import Hospital
from django.shortcuts import render 
from hospital.models import Appointment
def home(request):
    hospitals = Hospital.objects.all()
    print(hospitals)
    ctx = {
       "hospitals": hospitals
    }
    return render(request, 'home.html',context=ctx)
def get_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointments.html', {'appointments': appointments})