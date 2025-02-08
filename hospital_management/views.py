from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from hospital.models import Hospital
from django.shortcuts import render ,redirect
from hospital.models import Appointment,Prescription,User
from django.db.models import Q 
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
@login_required
def cancel_appointment(request,appointment_id):
    appointment = get_object_or_404(Appointment,id=appointment_id)
    
    appointment.delete()
    messages.success(request,"Appointment Cancelled Successfully")
    return redirect("patient_appointments")

def get_prescriptions(request):
    prescriptions = Prescription.objects.filter(patient=request.user).order_by('-created_at').all()
    return render(request, 'prescriptions.html', {'prescriptions': prescriptions})

def show_prescription(request, id):
      prescription = Prescription.objects.get(id=id)
      return render(request, 'show_prescription.html', {'prescription': prescription})

def search_results(request):
    query = request.GET.get("q","")
    hospitals = Hospital.objects.filter (
        Q(name__icontains=query) | Q(address__icontains=query)
    )
    doctors = User.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query),
        role="doctor"

    )
    return render(
        request,
        "hospital/search_results.html",
        {"query": query,"hospitals": hospitals,"doctors": doctors}
    )