from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('doctors/', views.manage_doctors, name='manage_doctors'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/edit/<int:docid>/', views.edit_doctor, name='edit_doctor'),
    path('doctors/delete/<int:docid>/', views.delete_doctor, name='delete_doctor'),
    path('patients/', views.manage_patients, name='manage_patients'),
    path('patients/delete/<int:pid>/', views.delete_patient, name='delete_patient'),
    path('schedule/', views.manage_schedule, name='manage_schedule'),
    path('schedule/add/', views.add_schedule, name='add_schedule'),
    path('schedule/delete/<int:scheduleid>/', views.delete_schedule, name='delete_schedule'),
    path('appointments/', views.view_appointments, name='view_appointments'),
]
