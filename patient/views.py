from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from datetime import date, datetime
from accounts.decorators import login_required_patient
from accounts.models import WebUser
from .models import Patient
from doctor.models import Doctor, Specialties
from admin_panel.models import Schedule, Appointment


def get_patient(request):
    """Helper function to get logged-in patient"""
    email = request.session.get('user')
    return Patient.objects.select_related('pemail').get(pemail=email)


@login_required_patient
def dashboard(request):
    """Patient dashboard home"""
    patient = get_patient(request)

    # Get statistics
    total_appointments = Appointment.objects.filter(pid=patient).count()
    upcoming_sessions = Schedule.objects.filter(
        scheduledate__gte=date.today()
    ).count()
    total_doctors = Doctor.objects.count()

    # Get recent appointments
    recent_appointments = Appointment.objects.filter(
        pid=patient
    ).select_related('scheduleid', 'scheduleid__docid').order_by('-appodate')[:5]

    context = {
        'patient': patient,
        'total_appointments': total_appointments,
        'upcoming_sessions': upcoming_sessions,
        'total_doctors': total_doctors,
        'recent_appointments': recent_appointments,
    }
    return render(request, 'patient/dashboard.html', context)


@login_required_patient
def all_doctors(request):
    """View all doctors with search"""
    patient = get_patient(request)

    # Get all doctors with specialties
    doctors = Doctor.objects.select_related('specialties', 'docemail').all()

    # Search functionality
    search_query = request.GET.get('search', '') or request.POST.get('search', '')
    if search_query:
        doctors = doctors.filter(
            Q(docname__icontains=search_query) |
            Q(docemail__email__icontains=search_query)
        )

    # Get all doctor names and emails for datalist
    all_doctors = Doctor.objects.select_related('docemail').all()
    doctor_suggestions = []
    for doc in all_doctors:
        doctor_suggestions.append(doc.docname)
        doctor_suggestions.append(doc.docemail.email)

    context = {
        'patient': patient,
        'doctors': doctors,
        'search_query': search_query,
        'doctor_suggestions': doctor_suggestions,
    }
    return render(request, 'patient/all_doctors.html', context)


@login_required_patient
def scheduled_sessions(request):
    """View scheduled sessions and book appointments"""
    patient = get_patient(request)

    # Get all upcoming schedules
    schedules = Schedule.objects.filter(
        scheduledate__gte=date.today()
    ).select_related('docid', 'docid__specialties').order_by('scheduledate', 'scheduletime')

    # Date filter
    filter_date = request.GET.get('date', '')
    if filter_date:
        schedules = schedules.filter(scheduledate=filter_date)

    # Doctor name filter (from Sessions button on All Doctors page)
    doctor_name = request.GET.get('doctor', '')
    if doctor_name:
        schedules = schedules.filter(docid__docname__icontains=doctor_name)

    # Handle booking
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        if schedule_id:
            schedule = get_object_or_404(Schedule, scheduleid=schedule_id)

            # Calculate next appointment number
            existing_count = Appointment.objects.filter(scheduleid=schedule).count()
            next_apponum = existing_count + 1

            # Check if slots available
            if next_apponum <= schedule.nop:
                # Create appointment
                appointment = Appointment.objects.create(
                    pid=patient,
                    apponum=next_apponum,
                    scheduleid=schedule,
                    appodate=date.today()
                )

                context = {
                    'patient': patient,
                    'schedules': schedules,
                    'filter_date': filter_date,
                    'doctor_name': doctor_name,
                    'success': True,
                    'appointment_number': appointment.apponum,
                    'schedule_title': schedule.title,
                }
                return render(request, 'patient/scheduled_sessions.html', context)
            else:
                context = {
                    'patient': patient,
                    'schedules': schedules,
                    'filter_date': filter_date,
                    'doctor_name': doctor_name,
                    'error': 'No slots available for this session',
                }
                return render(request, 'patient/scheduled_sessions.html', context)

    context = {
        'patient': patient,
        'schedules': schedules,
        'filter_date': filter_date,
        'doctor_name': doctor_name,
    }
    return render(request, 'patient/scheduled_sessions.html', context)


@login_required_patient
def my_bookings(request):
    """View my appointments"""
    patient = get_patient(request)

    # Get all appointments
    appointments = Appointment.objects.filter(
        pid=patient
    ).select_related(
        'scheduleid',
        'scheduleid__docid',
        'scheduleid__docid__specialties'
    ).order_by('-appodate')

    # Date filter
    filter_date = request.GET.get('date', '')
    if filter_date:
        appointments = appointments.filter(appodate=filter_date)

    context = {
        'patient': patient,
        'appointments': appointments,
        'filter_date': filter_date,
    }
    return render(request, 'patient/my_bookings.html', context)


@login_required_patient
def cancel_appointment(request, appoid):
    """Cancel an appointment"""
    patient = get_patient(request)
    appointment = get_object_or_404(Appointment, appoid=appoid, pid=patient)

    if request.method == 'POST':
        appointment.delete()
        return redirect('/patient/appointment/?cancelled=true')

    context = {
        'patient': patient,
        'appointment': appointment,
    }
    return render(request, 'patient/cancel_appointment.html', context)


@login_required_patient
def settings(request):
    """Patient settings page"""
    patient = get_patient(request)

    context = {
        'patient': patient,
    }
    return render(request, 'patient/settings.html', context)


@login_required_patient
def edit_settings(request):
    """Edit patient settings"""
    patient = get_patient(request)

    if request.method == 'POST':
        # Update patient info
        patient.pname = request.POST.get('pname', patient.pname)
        patient.paddress = request.POST.get('paddress', patient.paddress)
        patient.pnic = request.POST.get('pnic', patient.pnic)
        patient.ptel = request.POST.get('ptel', patient.ptel)
        patient.pdob = request.POST.get('pdob', patient.pdob)
        patient.save()

        # Update session username
        request.session['username'] = patient.pname.split()[0]

        return redirect('/patient/settings/?updated=true')

    context = {
        'patient': patient,
    }
    return render(request, 'patient/edit_settings.html', context)


@login_required_patient
def delete_account(request):
    """Delete patient account"""
    patient = get_patient(request)

    if request.method == 'POST':
        email = patient.pemail.email

        # Delete patient record (cascades to appointments)
        patient.delete()

        # Delete WebUser record
        WebUser.objects.filter(email=email).delete()

        # Flush session
        request.session.flush()

        return redirect('/login/?deleted=true')

    context = {
        'patient': patient,
    }
    return render(request, 'patient/delete_account.html', context)
