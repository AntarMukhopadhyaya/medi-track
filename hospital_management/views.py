
from hospital.models import Hospital
from django.shortcuts import render 

def home(request):
    hospitals = Hospital.objects.all()
    print(hospitals)
    ctx = {
       "hospitals": hospitals
    }
    return render(request, 'home.html',context=ctx)