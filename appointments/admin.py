from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from appointments.models import Appointment
from appointments.forms import AppointmentCreationForm, AppointmentUpdateForm


# class UserAdmin(BaseUserAdmin):
#     # # The forms to add and change appointments instances
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('appointment_id', 'doctor_email', 'patient_email', f'due_date', 'creation_date')
#     list_filter = ('due_date', )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     search_fields = ('doctor_email', 'patient_email')
#     ordering = ('due_date',)
#     filter_horizontal = ()


admin.site.register(Appointment)
