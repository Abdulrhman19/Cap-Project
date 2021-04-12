from django import forms
from .models import Appointment

from users.models import Doctor, Patient

class AppointmentCreationForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'doctor_id',
            'appointment_reason',
            'due_date',
        ]

class AppointmentStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('status',)