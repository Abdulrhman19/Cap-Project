from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

from .models import Patient, Doctor, Pharmacist, LabTechnician

User = get_user_model()

# class UserCreationForm(forms.ModelForm):
#     # role = forms.ChoiceField(widget=forms.RadioSelect, choices=[(1, 'Patient'), (2, 'Doctor')])
#     class Meta:
#         model = User
#         fields = ('email', 'password, ')

class PatientCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
    class Meta:
        model  = Patient
        fields = '__all__'

class DoctorCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
    class Meta:
        model  = Doctor
        fields = '__all__'


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin', 'role')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class PatientHealthUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = (
            'date_of_birth',
            'age', 
            'gender',     
            'weight',     
            'height',     
            'blood_group',
            'country',    
            'city',       
            'street',     
        )

class PatientPersonalUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'personal_image')


class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = (
            'specialist',
            'gender',
        )

class DoctorPersonalUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'personal_image')