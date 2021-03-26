
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    # ? create_user( takes all the required fileds )
    def create_user(self, email, is_staff, is_admin, is_doctor=False, is_patient=False, password=None, is_active=True):

        if not password:
            raise ValueError("Users must have a password")

        if not email:
            raise ValueError("Users must have an email address")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.doctor = is_doctor
        user_obj.patient = is_patient
        user_obj.actvie = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,  email, password=None):
        user = self.create_user(email, password=password, is_staff=True)
        return user

    def create_superuser(self,  email, password=None):
        user = self.create_user(email, password=password,
                                is_admin=True, is_staff=True)
        return user

    def create_patient(self,  email, password=None):
        user = self.create_user(email, password=password, is_patient=True)
        return user

    def create_doctor(self,  email, password=None):
        user = self.create_user(email, password=password, is_doctor=True)
        return user


class User(AbstractBaseUser):

    USER_TYPE = (
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
    )

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  # ? Can login?
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    role = models.CharField(max_length=8, choices=USER_TYPE)

    USERNAME_FIELD = 'email'
    # * USERNAME_FIELDS(Email) and Password are required by default
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        return "%s" % (self.first_name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specifit permissions ?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_patient(self):
        return self.patient

    @property
    def is_doctor(self):
        return self.doctor


class Patinet(models.Model):

    # TODO: Add doctor

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    patinet = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    supervised_by = models.ForeignKey(
        "Doctor", on_delete=models.CASCADE, blank=True)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=6, choices=GENDER)
    weight = models.FloatField()
    height = models.FloatField()
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    street = models.CharField(max_length=60)
    # image = models.ImageField("Patient personal image", )

    def __str__(self):
        return self.patinet.email

    def get_patient_location(self):
        return f"{self.city}, {self.country}"


class Doctor(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    doctor           = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Doctor')
    specialist       = models.CharField(max_length=255)
    gender           = models.CharField(max_length=6, choices=GENDER)


    def __str__(self):
        return self.doctor.email

class LabTechnician(models.Model):
    lab_technician              = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_case                   = models.TextField(max_length=255)
    test_name                   = models.TextField(max_length=255)
    test_cost                   = models.FloatField()


class Pharmacist(models.Model):
    pharmacist              = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    drug_presription        = models.TextField(max_length=255)
    drug_instruction        = models.TextField(max_length=512)
    drug_cost               = models.FloatField()


