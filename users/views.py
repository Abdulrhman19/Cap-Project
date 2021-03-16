from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import (
    UserAdminCreationForm,
    # UserCreationForm,
    PatientCreationForm,
    DoctorCreationForm
)

from .models import Patinet, Doctor, User, UserManager

User = get_user_model()


def landing_page(request):
    return render(request, 'landing_page.html', {})


def signup_view(request):
    form = UserAdminCreationForm()
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            form.save()

            # Check user role
            if form.cleaned_data['role'] == 'Patient':
                patient_signup_view(request)
                return redirect('/register_patient/')
                print(form.cleaned_data)
            elif form.cleaned_data['role'] == 'Doctor':
                doctor_signup_view(request)
                return redirect('/register_doctor/')
                print(form.cleaned_data)

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
            
            new_patient = Patinet.objects.create(
                patinet=patient,
                supervised_by=supervised_by,
                date_of_birth=date_of_birth,
                age=age,
                gender=gender,
                weight=weight,
                height=height,
                country=country,
                city=city,
                street = street,
            )

            Patinet.save(new_patient)
            return redirect('/login/')
        else:
            print("Make sure to complete the form before submitting it!")
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
    print("In the view")
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            print("Validation ...")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                print("Pass all tests")
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('/')
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
