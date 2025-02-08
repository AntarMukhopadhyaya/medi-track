from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Appointment


@receiver(post_save, sender=Appointment)
def send_appointment_confirmation(sender, instance, **kwargs):
    if instance.status == "confirmed":
        subject = "Your Appointment is Confirmed"
        message = f"Dear {instance.patient.first_name},\n\n" \
            f"Your appointment with Dr. {instance.doctor.first_name} on {instance.date} at {instance.time} has been confirmed with appointment number {instance.id}.\n\n" \
            f"Thank you for choosing our hospital.\n\nBest Regards,\nHospital Management"
        recipient_email = instance.patient.email

        send_mail(subject, message, "your-email@gmail.com", [recipient_email])
    elif instance.status == "cancelled":
        subject = "Your Appointment is Cancelled"
        message = f"Dear {instance.patient.first_name},\n\n" \
            f"Your appointment with Dr. {instance.doctor.first_name} on {instance.date} at {instance.time} has been cancelled.\n\n" \
            f"Sorry for the inconvenience caused.\n\nBest Regards,\nHospital Management"
        recipient_email = instance.patient.email

        send_mail(subject, message, "your-email@gmail.com", [recipient_email])
