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
    
    # * Patient pages
    path('patient/<int:patient_id>/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/<int:patient_id>/profile/', views.patient_profile, name='patient_profile'),
    path('patient/<int:patient_id>/maps/', views.maps, name='maps'),

    # * Doctor pages
    path('doctor/<int:doctor_id>/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctors/delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('doctor/<int:doctor_id>/profile/', views.doctor_profile, name='doctor_profile'),

]
