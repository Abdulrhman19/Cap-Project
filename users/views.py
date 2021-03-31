from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from random import randint
from .forms import (
    UserAdminCreationForm,
    # UserCreationForm,
    PatientCreationForm,
    DoctorCreationForm
)

from .models import Patient, Doctor, User, UserManager

User = get_user_model()


def landing_page(request):
    return render(request, 'landing_page.html', {})


def signup_view(request):
    form = UserAdminCreationForm()  # GET REQUEST
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)
        print(form)
        if form.is_valid():

            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            form.save()

            # Check user role
            if form.cleaned_data['role'] == 'Patient':
                patient_signup_view(request)
                return redirect('/register_patient/')
            elif form.cleaned_data['role'] == 'Doctor':
                doctor_signup_view(request)
                return redirect('/register_doctor/')
        else:
            messages.error(request, "You must select a role")

    return render(request, 'registration/signup.html', {'form': form})


def patient_signup_view(request):
    form = PatientCreationForm()

    if request.method == 'POST':
        form = PatientCreationForm(request.POST)

        if form.is_valid():
            patient = User.objects.filter(
                role='Patient').order_by('-date_joined').first()
            supervised_by = form.cleaned_data['supervised_by']
            date_of_birth = form.cleaned_data['date_of_birth']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']

            new_patient = Patient.objects.create(
                patient=patient,
                supervised_by=supervised_by,
                date_of_birth=date_of_birth,
                age=age,
                gender=gender,
                weight=weight,
                height=height,
                country=country,
                city=city,
                street=street,
            )

            patient.save(new_patient)
            return redirect('/login/')
        else:
            messages.error(request, "Make sure to complete the form before submitting it!")
    return render(request, 'registration/patient_signup.html', {'form': form})


def doctor_signup_view(request):
    form = DoctorCreationForm()

    if request.method == 'POST':
        form = DoctorCreationForm(request.POST)

        if form.is_valid():
            doctor = User.objects.order_by('-date_joined').first()
            specialist = form.cleaned_data['specialist']
            new_doctor = Doctor.objects.create(
                doctor=doctor, specialist=specialist)
            Doctor.save(new_doctor)
            return redirect('/login/')
        else:
            print("Invalid")
    return render(request, 'registration/doctor_signup.html', {'form': form, })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            print("Validation ...")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # user: is an email.
                login(request, user)
                print(user, type(user))
                messages.info(request, f"You are now logged in as {username}.")

                # If the logged in user is patient redirect them for patient dashboard
                # other wise to doctor dashboard
                # TODO: Users [Admin, Doctor, Patient] redirected to patient Dashboard after logging.
                # TODO: It need's to be fixed by tonight.

                if User.objects.get(email=user).admin == True:
                    # Admin user/admin/'
                    return redirect('http://127.0.0.1:8000/admin/')
                elif User.objects.get(email=user).role == 'Patient':
                    # patient user
                    return redirect('users:patient_dashboard')
                elif User.objects.get(email=user).role == 'Doctor':
                    return redirect('users:doctor_dashboard')

            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    # messages.info(request, 'You have been logged out.')
    return redirect('/')


# PATIENT DASHBAORD FUNCTIONS
@login_required
def patient_dashboard(request):
    current_patient = request.user
    patient = Patient.objects.get(patient=current_patient)

    gender, height, weight, age = (
        patient.gender,
        patient.height,
        patient.weight,
        patient.age,
    )

    # Custom values
    body_mass_index = round(weight / ((height / 100) ** 2), 2)
    diabetes_level = randint(140, 200)
    blood_pressure = {
        'systolic': randint(120, 140),
        'diastolic': randint(80, 90),
    }
    steps = randint(1000, 10000)

    context = {
        'gender': gender,
        'height': height,
        'weight': weight,
        'age': age,
        'bmi': body_mass_index,
        'diabetes_level': diabetes_level,
        'blood_pressure': blood_pressure,
        'steps': steps,
    }
    return render(request, 'users/patient/dashboard_content.html', context)


@login_required
def maps(request):
    # Return all the clinics in a 'city' in google maps.
    patient = patient.objects.get(pk=1)
    country = patient.country
    city = patient.city

    context = {
        'country': country,
        'city': city,
    }
    return render(request, 'users/patient/map.html', context)


@login_required
def patient_profile(request):
    pass
# END PATIENT VIEWS


# DOCTOR DASHBAORD FUNCTIONS
@login_required
def doctor_dashboard(request):
    current_doctor = request.user
    doctor = Doctor.objects.get(doctor=current_doctor)
    patients = doctor.patient_set.all()

    context = {
        'patients': patients,
    }
    return render(request, 'users/doctor/dashboard_content.htm', context)


@login_required
def delete_patient(request, patient_id):
    print("Inside function")
    current_doctor = Doctor.objects.get(doctor=request.user)
    patient = current_doctor.patient_set.get(id=patient_id)
    Doctor.delete(patient)
    messages.success(request, f"{patient} has been removed.")
    return HttpResponseRedirect(reverse("users:doctor_dashboard"))
# END DOCTOR VIEWS
