from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from datetime import date, datetime, time
from accounts.decorators import login_required_doctor
from .models import Doctor
from admin_panel.models import Schedule, Appointment


def get_doctor(request):
    """Helper function to get logged-in doctor"""
    email = request.session.get('user')
    return Doctor.objects.select_related('docemail', 'specialties').get(docemail=email)


@login_required_doctor
def dashboard(request):
    """Doctor dashboard home"""
    doctor = get_doctor(request)

    # Get statistics
    total_sessions = Schedule.objects.filter(docid=doctor).count()
    total_appointments = Appointment.objects.filter(
        scheduleid__docid=doctor
    ).count()

    # Get today's date
    today = date.today()

    context = {
        'doctor': doctor,
        'total_sessions': total_sessions,
        'total_appointments': total_appointments,
        'today': today,
    }
    return render(request, 'doctor/dashboard.html', context)


@login_required_doctor
def schedule(request):
    """Manage doctor's own sessions"""
    doctor = get_doctor(request)

    # Get all schedules for this doctor with appointment counts
    schedules = Schedule.objects.filter(docid=doctor).annotate(
        appointment_count=Count('appointment')
    ).order_by('-scheduledate', '-scheduletime')

    context = {
        'doctor': doctor,
        'schedules': schedules,
    }
    return render(request, 'doctor/schedule.html', context)


@login_required_doctor
def add_schedule(request):
    """Add new session"""
    doctor = get_doctor(request)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        schedule_date = request.POST.get('scheduledate', '').strip()
        schedule_time = request.POST.get('scheduletime', '').strip()
        nop = request.POST.get('nop', '').strip()

        # Validate inputs
        if not all([title, schedule_date, schedule_time, nop]):
            context = {
                'doctor': doctor,
                'error': 'All fields are required',
            }
            return render(request, 'doctor/add_schedule.html', context)

        try:
            # Create schedule
            Schedule.objects.create(
                docid=doctor,
                title=title,
                scheduledate=schedule_date,
                scheduletime=schedule_time,
                nop=int(nop)
            )
            return redirect('/doctor/schedule/?added=true')
        except Exception as e:
            context = {
                'doctor': doctor,
                'error': f'Error creating schedule: {str(e)}',
            }
            return render(request, 'doctor/add_schedule.html', context)

    # GET request
    context = {
        'doctor': doctor,
    }
    return render(request, 'doctor/add_schedule.html', context)


@login_required_doctor
def delete_schedule(request, scheduleid):
    """Delete a session"""
    doctor = get_doctor(request)
    schedule = get_object_or_404(Schedule, scheduleid=scheduleid, docid=doctor)

    # Check if appointments exist
    appointment_count = Appointment.objects.filter(scheduleid=schedule).count()

    if request.method == 'POST':
        if appointment_count > 0:
            # Show error if appointments exist
            return redirect(f'/doctor/schedule/?error=Cannot delete session with existing appointments')

        schedule.delete()
        return redirect('/doctor/schedule/?deleted=true')

    context = {
        'doctor': doctor,
        'schedule': schedule,
        'appointment_count': appointment_count,
    }
    return render(request, 'doctor/delete_schedule.html', context)


@login_required_doctor
def appointments(request):
    """View appointments for doctor's sessions"""
    doctor = get_doctor(request)

    # Get all appointments for this doctor's sessions
    appointments = Appointment.objects.filter(
        scheduleid__docid=doctor
    ).select_related(
        'pid',
        'pid__pemail',
        'scheduleid'
    ).order_by('-appodate', 'scheduleid__scheduledate')

    # Date filter
    filter_date = request.GET.get('date', '')
    if filter_date:
        appointments = appointments.filter(appodate=filter_date)

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'filter_date': filter_date,
    }
    return render(request, 'doctor/appointments.html', context)
