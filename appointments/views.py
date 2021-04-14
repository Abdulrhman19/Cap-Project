from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
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


@login_required
def appointment_create_view(request):

    # Get all the existing doctor
    doctors = Doctor.objects.all()

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
            messages.error(request, f"{form.errors}")
        print(form)
    return render(request, 'appointments/new_appointment.html', {'form': form, 'doctors': doctors})


def delete_appointment(request, appointment_pk):
    patient = request.user.Patient.id
    # appointments = Appointment.objects.filter(patient_id=patient)
    print("+++IN")
    appointment = Appointment.objects.get(pk=appointment_pk)
    if appointment.status == 'Accepted':
        print("Do not print")
    else:
        print(f"+++{appointment}")
        Appointment.delete(appointment)
        messages.success(request, f"Appointment has been removed.")
        return redirect("users:patient_dashboard", request.user.Patient.id)


# TODO: Appointment status must be fixed as fast as you can


def reject_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    print(appointment.status)
    appointment.status = 'Rejected'
    Appointment.save(appointment)
    print(appointment.status)
    return redirect("appointments:requested_appointments")


def accept_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    print(appointment.status)
    appointment.status = 'Accepted'
    Appointment.save(appointment)
    print(appointment.status)
    return redirect("appointments:requested_appointments")



def patient_appointments(patient_id):
    patient = Patient.objects.get(id=patient_id)
    appointments = patient.appointment_set.all()
    return list(appointments)


def doctor_appointments(doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    appointments = doctor.appointment_set.all()
    return list(appointments)
