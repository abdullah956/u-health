from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/add/', views.add_schedule, name='add_schedule'),
    path('schedule/delete/<int:scheduleid>/', views.delete_schedule, name='delete_schedule'),
    path('appointments/', views.appointments, name='appointments'),
]
