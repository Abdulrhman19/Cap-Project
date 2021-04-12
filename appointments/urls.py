from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('new_appointemnt/', views.appointment_create_view, name='new_appointemnt'),
    path('patient_appointments/', views.patient_appointments, name='patient_appointments'),
    path('requested_appointments/', views.DoctorAppointmentsListView.as_view(), name='requested_appointments'),
    path('get_appointment_status/', views.get_appointment_status, name='get_appointment_status'),
]