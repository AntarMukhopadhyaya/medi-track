from .forms import UserRegisterForm,FeedbackForm
from django.contrib.auth.models import Group

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Hospital, OPDQueue, BedQueue, User,Feedback,Prescription,Department,Medicine,Appointment
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.timezone import now



@login_required
def opd_queue(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    opd_patients = OPDQueue.objects.filter(
        hospital=hospital,status="waiting").order_by('priority','created_at')
    return render(request, 'hospital/opdqueue.html', {'hospital': hospital, 'opd_patients': opd_patients})

@login_required
def opd_queue_update(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    opd_patients = OPDQueue.objects.filter(hospital=hospital,status="waiting").order_by('priority','created_at')
    return render(request, 'partials/opdlist.html', {'hospital': hospital, 'opd_patients': opd_patients})

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


def department_list(request):
    departments = Department.objects.all()
    return render(request, "hospital/departments.html", {"departments": departments})

def department_detail(request, department_id):
    department = Department.objects.get(id=department_id)
    doctors = User.objects.filter(department=department, role="doctor")
    patients = User.objects.filter(department=department, role="patient")
    return render(request, "hospital/department_detail.html", {"department": department, "doctors": doctors, "patients": patients})

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Successfully logged out.")
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
        hospital=hospital,status="waiting").order_by('priority','created_at').first()
    if next_patient:
        next_patient.status = "in_consultation"
        next_patient.save()
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
        if Appointment.objects.filter(doctor_id=doctor_id,date=date,time=time).exists():
            messages.error(request,"Doctor is not available at this time")
            return redirect('home')
        appointment = Appointment.objects.create(
            patient=patient,
            doctor_id=doctor_id,
            hospital_id=hospital_id,
            date=date,
            time=time,
            reason=reason
        )
        messages.success(request, "Appointment booked successfully! Once confirmed a mail will be sent to you")

        return redirect('home')
    return redirect("/login")


@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.patient = request.user  # Set the patient
            feedback.save()
            return redirect('feedback_list')  # Redirect to feedback list
    else:
        form = FeedbackForm()

    recipients = User.objects.filter(role__in=["doctor","staff"])  # Only allow feedback to doctors & staff
    return render(request, 'hospital/submit_feedback.html', {'form': form, 'recipients': recipients})


@login_required
def feedback_list(request):
    if request.user.role == 'doctor' or request.user.role == 'staff':
        feedbacks = Feedback.objects.filter(recipient=request.user)  # Show feedback received
    else:
        feedbacks = Feedback.objects.filter(patient=request.user)  # Show feedback given

    return render(request, 'hospital/feedback_list.html', {'feedbacks': feedbacks})



@login_required
def schedule_later(request, queue_id):
    queue_entry = get_object_or_404(OPDQueue, id=queue_id)
    
    # Move the patient to the end of the queue by updating created_at
    queue_entry.created_at = now()
    queue_entry.save()

    return opd_queue_update(request)

@login_required
def generate_prescription(request,queue_id):
    queue = get_object_or_404(OPDQueue, id=queue_id)
    medicines = Medicine.objects.all().order_by('name')
    if request.method == "POST":
        age = request.POST.get('age')
        content = request.POST.get('content')
        weight = request.POST.get('weight')

        from .models import Prescription
        if Prescription.objects.create(
            patient=queue.patient,
            doctor=request.user,
            hospital=queue.hospital,
            age=age,
            weight=weight,
            content=content
        ):
            queue.status = "completed"
            queue.save()
            messages.success(request, "Prescription generated successfully!")
            return redirect('opd_queue', hospital_id=queue.hospital.id)
        else:
            messages.error(request, "Failed to generate prescription!")
            return redirect('opd_queue', hospital_id=queue.hospital.id)
    return render(request, 'hospital/generate_prescription.html', {'queue': queue,"medicines":medicines})


@login_required 
def doctor_dashboard(request):
    if request.user.role == 'doctor':
        doctor = request.user  # Get the logged-in doctor
        opd_patients = OPDQueue.objects.filter(doctor=doctor).order_by("created_at")
        prescriptions = Prescription.objects.filter(doctor=doctor).order_by("-created_at")
        context = {
        "doctor": doctor,
        "opd_patients": opd_patients,
        "prescriptions": prescriptions,
        }
        return render(request, 'dashboard/doctor.html', context)
    else:
        return redirect('home')


    
