from django.urls import path
from . import views
app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('user_role/', views.get_user_role, name='user_role'),
    path('signup/', views.signup_view, name='signup'),
    path('register_patient/', views.patient_signup_view, name='patient_signup'),
    path('register_doctor/', views.doctor_signup_view, name='doctor_signup'),
]