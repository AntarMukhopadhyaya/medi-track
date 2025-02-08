from django.contrib import admin
from django.db.models import Q
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from .models import User, Hospital, Appointment, OPDQueue, Feedback, Department, Medicine, Prescription
from django.db.models import Count
from datetime import datetime
from django.utils.html import format_html
admin.site.site_header = "Hospital Management Admin"
admin.site.site_title = "Hospital Dashboard"
admin.site.index_title = "Welcome to Hospital Management System"


class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role',
                    'hospital', "monthly_appointments", 'abha_id')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('hospital', 'role',"department")}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', "department", 'password1', 'password2', 'hospital', 'role', 'is_staff', 'is_superuser')}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'abha_id',"department")
    ordering = ('email', 'first_name', 'last_name')

    def get_queryset(self, request):
        """Annotate each doctor with their appointment count for the current month."""
        qs = super().get_queryset(request)
        now = timezone.localtime(timezone.now())

        return qs.annotate(
            monthly_appointments_count=Count(
                "doctor_appointments",  # ✅ Correct related name,
                filter=Q(doctor_appointments__date__month=now.month,
                         doctor_appointments__date__year=now.year)
            )
        )

    def monthly_appointments(self, obj):
        return obj.monthly_appointments_count  # Access the annotated field

    monthly_appointments.admin_order_field = 'monthly_appointments_count'  # ✅ Enables sorting


# ✅ Register the CustomUser model with CustomUserAdmin
admin.site.register(User, CustomUserAdmin)


class AppointmentStatusFilter(admin.SimpleListFilter):
    title = "Appointment Status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
            ("rescheduled", "Rescheduled"),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "date", "time", "status","created_at")
    list_filter = ("date", "time", "status")  # Add default and status filters
    search_fields = ("patient__email", "patient__first_name", "patient__last_name",
                     # Fix: Required for autocomplete
                     "doctor__email", "doctor__first_name", "doctor__last_name")
    # Fix: Needs search_fields
    ordering = ["-date", "time"]


admin.site.register(Hospital)

admin.site.register(OPDQueue)
admin.site.register(Feedback)
admin.site.register(Department)
admin.site.register(Medicine)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "hospital",
                    "age", "weight", "created_at")
    list_filter = ("age", "weight", "created_at")
    search_fields = ("patient__first_name", "patient__email", "patient__last_name",
                     "patient__abha_id", "doctor__email", "doctor__first_name", "doctor__last_name")
    ordering = ["-created_at"]
