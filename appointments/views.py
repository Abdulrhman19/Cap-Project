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
from .forms import AppointmentCreationForm, AppointmentStatusUpdateForm
from .models import Appointment

User = get_user_model()


class DoctorAppointmentsListView(ListView):
    template_name = 'appointments/doctor_appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        appointments = self.request.user.Doctor.appointment_set.all().order_by('-due_date')
        return list(appointments)


def appointment_create_view(request):
    form = AppointmentCreationForm()
    if request.method == 'POST':
        form = AppointmentCreationForm(request.POST)
        if form.is_valid():
            patient_id = Patient.objects.get(patient=request.user)
            doctor_id = form.cleaned_data['doctor_id']
            appointment_reason = form.cleaned_data['appointment_reason']
            due_date = form.cleaned_data['due_date']

            new_appointment = Appointment.objects.create(
                doctor_id=doctor_id,
                patient_id=patient_id,
                appointment_reason=appointment_reason,
                due_date=due_date
            )

            Appointment.save(new_appointment)

            messages.success(
                request, f"Appointment request with Dr.{doctor_id.doctor.get_full_name()} has been sent.")
            return redirect('users:patient_dashboard', request.user.Patient.id)
        else:
            messages.error(request, f"Please make sure to enter valid data.")
    return render(request, 'appointments/new_appointment.html', {'form': form})


# TODO: Appointment status must be fixed as fast as you can
def get_appointment_status(request):
    form = AppointmentStatusUpdateForm()
    if request.method == 'POST':
        print("----POST")
        form = AppointmentStatusUpdateForm(request.POST)

        if form.is_valid():
            status = form.cleaned_data['status']
            print(status)

            patient = Patient.objects.get(id=request.user.Patient.id)
            doctor = Doctor.objects.get(id=request.user.Doctor.id)

            appointment = Appointment.objects.get(id=request.appointment.id)
            print(appointment)

            appointment.status = status
            print(appointment.status)

            Appointment.save(appointment)

            return redirect("appointments:requested_appointments")
        else:
            print(form.errors)
    else:
        print("+++++ GET")
    return render(request, 'appointments/doctor_appointments.html', {'form': form})
            
    
def patient_appointments(patient_id):
    patient = Patient.objects.get(id=patient_id)
    appointments = patient.appointment_set.all()
    return list(appointments)


def doctor_appointments(doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    appointments = doctor.appointment_set.all()
    return list(appointments)
