from django.db import models
from users.models import Doctor, Patient

class Appointment(models.Model):
    "A class to allow patients to reserve an appointments with their doctors"
    appointment_id         = models.AutoField(primary_key=True)   
    doctor_id              = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_id             = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_reason     = models.TextField("Appointment Reason", max_length=512)
    due_date               = models.DateTimeField("Due Date",auto_now_add=False)
    creation_date          = models.DateTimeField(auto_now_add=True)
    status                 = models.CharField(max_length=10, default='Pennded')


    def __str__(self):
        return f"Appointment number {self.appointment_id}"