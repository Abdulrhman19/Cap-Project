from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

from users.models import Patient, Doctor
from .forms import AppointmentCreationForm
from .models import Appointment

User = get_user_model()


def appointment_create_view(request):
    form = AppointmentCreationForm()
    if request.method == 'POST':
        form = AppointmentCreationForm(request.POST)
        if form.is_valid():
            patient_email = Patient.objects.get(patient=request.user)
            doctor_email = form.cleaned_data['doctor_email']
            appointment_reason = form.cleaned_data['appointment_reason']
            due_date = form.cleaned_data['due_date']

            new_appointment = Appointment.objects.create(
                doctor_email=doctor_email,
                patient_email=patient_email,
                appointment_reason=appointment_reason,
                due_date=due_date
            )

            Appointment.save(new_appointment)
 
            messages.success(request, f"Appointment request with Dr.{doctor_email.doctor.get_full_name()} has been sent.")
            return redirect('/')
        else:
            messages.error(request, f"Please make sure to enter valid data.")
    return render(request, 'appointments/new_appointment.html', {'form': form})


# def get_user_type(request):
#     user_type = ''
#     if request.user == 'Patient':
#         user_type = 'Patient'
#     elif request.user == 'Doctor':
#         user_type = 'Doctor'

#     return user_type



def patient_appointments(request):
    # user_type = get_user_type(request)
    context = {}
    if request.user.role == 'Patient':
        patient = Patient.objects.get(patient=request.user.id)
        appointments = Appointment.objects.filter(patient_id=patient.id)
        context['appointments'] = appointments    
        print(context)
    else:
        print("d")
        doctor_appointments(request)
    
    return render(request, 'appointments/patient_appointments.html', context)

def doctor_appointments(request):
    pass

        

