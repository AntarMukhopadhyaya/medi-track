from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

# Custom User Manager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Custom User Model


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    hospital = models.ForeignKey(
        'Hospital', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'),
        ('patient', 'Patient')
    ], default='patient')

    groups = models.ManyToManyField(
        Group, related_name="hospital_users", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="hospital_users_permissions", blank=True)
    abha_id = models.CharField(max_length=15, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} - {self.role}"


# Hospital Model
class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_doctors(self):
        return self.user_set.filter(role='doctor')

    def get_staff(self):
        return self.user_set.filter(role='staff')


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='doctor_appointments')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    duration = models.IntegerField(default=15)

    class Status(models.TextChoices):
        PENDING = "pending"
        CONFIRMED = "confirmed"
        COMPLETED = "completed"
        CANCELLED = "cancelled"
        RESCHEDULED = "rescheduled"

    status = models.CharField(choices=Status.choices,
                              default=Status.PENDING, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['date', 'time', 'doctor']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.add_patient_to_queue()

    def add_patient_to_queue(self):
        OPDQueue.objects.create(hospital=self.hospital,
                                patient=self.patient, doctor=self.doctor)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.doctor.first_name} - {self.date} - {self.time}"


class OPDQueue(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='doctor_opd_queue', null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.IntegerField(default=0)
    status = models.CharField(choices=[('waiting', 'Waiting'), ('in_consultation',
                              'In Consultation'), ('completed', 'Completed')], default='waiting', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['priority', 'created_at']

    def __str__(self):
        return f" {self.patient.first_name} {self.patient.last_name} - {self.created_at}"


class BedQueue(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['priority', 'created_at']

    def __str__(self):
        return f"{self.hospital.name} - {self.patient.email} - {self.priority} - {self.created_at}"


class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='doctor_prescriptions')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField(blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Feedback(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="feedbacks")
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_feedback")
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.patient} to {self.recipient} - {self.rating} Stars"
