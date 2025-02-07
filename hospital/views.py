
from .forms import UserRegisterForm
from django.contrib.auth.models import Group

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Hospital, OPDQueue, BedQueue, User
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib import messages



def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()


def is_staff(user):
    return user.groups.filter(name='Staff').exists()


def is_patient(user):
    return user.groups.filter(name='Patient').exists()


@login_required
def opd_queue(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    opd_patients = OPDQueue.objects.filter(
        hospital=hospital).order_by('created_at')
    return render(request, 'hospital/opdqueue.html', {'hospital': hospital, 'opd_patients': opd_patients})


def show(request, id):
    hospital = Hospital.objects.get(id=id)
    doctors = hospital.get_doctors()
    return render(request, 'hospital/show.html', {'hospital': hospital, 'doctors': doctors})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'patient'  # Automatically assign 'patient' role
            user.save()

            # Assign user to the "Patient" group
            patient_group, created = Group.objects.get_or_create(
                name='Patient')
            user.groups.add(patient_group)

            login(request, user)  # Auto-login after registration
            return redirect('home')  # Redirect to the dashboard
    else:
        form = UserRegisterForm()
    return render(request, 'hospital/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
      email = request.POST.get("email")
  
      password = request.POST.get("password")
      if User.objects.filter(email=email).exists():
            user = authenticate( email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
      else:
          messages.error(request,"No Such email exists")

    return render(request,"hospital/login.html")


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")
    return redirect("home")


def join_opd_queue(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    OPDQueue.objects.create(hospital=hospital, patient=request.user)
    return redirect('opd_queue', hospital_id=hospital_id)


@login_required
def serve_next_opd(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    next_patient = OPDQueue.objects.filter(
        hospital=hospital).order_by('created_at').first()
    if next_patient:
        next_patient.delete()
    return redirect('opd_queue', hospital_id=hospital_id)

### BED QUEUE (Priority-Based) ###


@login_required
def bed_queue(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    bed_patients = BedQueue.objects.filter(
        hospital=hospital).order_by('priority', 'created_at')
    return render(request, 'hospital/bed_queue.html', {'hospital': hospital, 'bed_patients': bed_patients})


@login_required
def join_bed_queue(request, hospital_id, priority):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    BedQueue.objects.create(
        hospital=hospital, patient=request.user, priority=priority)
    return redirect('bed_queue', hospital_id=hospital_id)


@login_required
def admit_next_patient(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    next_patient = BedQueue.objects.filter(
        hospital=hospital).order_by('priority', 'created_at').first()
    if next_patient:
        next_patient.delete()
    return redirect('bed_queue', hospital_id=hospital_id)


@login_required

def book_appointment(request):
    if request.method == "POST":
        from .models import User
        patient = User.objects.get(id=request.user.id)
        doctor_id = request.POST.get('doctor')
        hospital_id = request.POST.get('hospital_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')

        from .models import Appointment
        appointment = Appointment.objects.create(
            patient=patient,
            doctor_id=doctor_id,
            hospital_id=hospital_id,
            date=date,
            time=time,
            reason=reason
        )

        return redirect('home')
    return redirect("/login")
