from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail,EmailMultiAlternatives
from .models import Appointment,Prescription
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Prescription


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

        send_mail(subject, message, instance.hospital.email, [recipient_email])

@receiver(post_save, sender=Prescription)
def send_prescription_email(sender, instance, created, **kwargs):
    if created:  # Ensures email is only sent when a new prescription is created
        subject = "Your Prescription from Dr. {}".format(instance.doctor.first_name)
        
        # Render HTML email template
        html_message = render_to_string("prescription_email.html", {"prescription": instance})
        plain_message = strip_tags(html_message)
        
        email = EmailMultiAlternatives(subject, plain_message, "mukhopadhyayaantar@gmail.com", [instance.patient.email])
        email.attach_alternative(html_message, "text/html")
        email.send()

@receiver(pre_delete, sender=Appointment)
def remove_patient_from_queue_on_delete(sender, instance, **kwargs):
    instance.remove_patient_from_queue()