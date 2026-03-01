from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('doctors/', views.all_doctors, name='all_doctors'),
    path('schedule/', views.scheduled_sessions, name='scheduled_sessions'),
    path('appointment/', views.my_bookings, name='my_bookings'),
    path('appointment/cancel/<int:appoid>/', views.cancel_appointment, name='cancel_appointment'),
    path('settings/', views.settings, name='settings'),
    path('settings/edit/', views.edit_settings, name='edit_settings'),
    path('settings/delete/', views.delete_account, name='delete_account'),
]
