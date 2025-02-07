from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Hospital,Appointment,OPDQueue

class CustomUserAdmin(UserAdmin):
    list_display = ('first_name','last_name','username','email', 'role', 'hospital', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('hospital', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','email', 'password1', 'password2', 'hospital', 'role', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Hospital)
admin.site.register(Appointment)
admin.site.register(OPDQueue)
