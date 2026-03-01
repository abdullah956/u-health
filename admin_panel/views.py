from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from accounts.decorators import login_required_admin
from accounts.models import WebUser
from doctor.models import Doctor, Specialties
from patient.models import Patient
from .models import Schedule, Appointment


@login_required_admin
def dashboard(request):
    """Admin dashboard with statistics"""
    # Get statistics
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_sessions = Schedule.objects.count()
    total_appointments = Appointment.objects.count()

    context = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_sessions': total_sessions,
        'total_appointments': total_appointments,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required_admin
def manage_doctors(request):
    """List all doctors"""
    doctors = Doctor.objects.select_related('specialties', 'docemail').all()

    context = {
        'doctors': doctors,
    }
    return render(request, 'admin_panel/manage_doctors.html', context)


@login_required_admin
def add_doctor(request):
    """Add new doctor"""
    specialties = Specialties.objects.all()

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        nic = request.POST.get('nic', '').strip()
        phone = request.POST.get('phone', '').strip()
        specialty_id = request.POST.get('specialty', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Validation
        if not all([email, name, nic, phone, specialty_id, password, confirm_password]):
            context = {
                'specialties': specialties,
                'error': 'All fields are required',
            }
            return render(request, 'admin_panel/add_doctor.html', context)

        if password != confirm_password:
            context = {
                'specialties': specialties,
                'error': 'Passwords do not match',
            }
            return render(request, 'admin_panel/add_doctor.html', context)

        if WebUser.objects.filter(email=email).exists():
            context = {
                'specialties': specialties,
                'error': 'Email already exists',
            }
            return render(request, 'admin_panel/add_doctor.html', context)

        try:
            # Create WebUser
            web_user = WebUser.objects.create(email=email, usertype='d')

            # Create Doctor
            specialty = Specialties.objects.get(id=specialty_id)
            Doctor.objects.create(
                docemail=web_user,
                docname=name,
                docpassword=password,
                docnic=nic,
                doctel=phone,
                specialties=specialty
            )

            return redirect('/admin-panel/doctors/?added=true')
        except Exception as e:
            context = {
                'specialties': specialties,
                'error': f'Error creating doctor: {str(e)}',
            }
            return render(request, 'admin_panel/add_doctor.html', context)

    # GET request
    context = {
        'specialties': specialties,
    }
    return render(request, 'admin_panel/add_doctor.html', context)


@login_required_admin
def edit_doctor(request, docid):
    """Edit existing doctor"""
    doctor = get_object_or_404(Doctor, docid=docid)
    specialties = Specialties.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        nic = request.POST.get('nic', '').strip()
        phone = request.POST.get('phone', '').strip()
        specialty_id = request.POST.get('specialty', '').strip()

        if not all([name, nic, phone, specialty_id]):
            context = {
                'doctor': doctor,
                'specialties': specialties,
                'error': 'All fields are required',
            }
            return render(request, 'admin_panel/edit_doctor.html', context)

        try:
            specialty = Specialties.objects.get(id=specialty_id)
            doctor.docname = name
            doctor.docnic = nic
            doctor.doctel = phone
            doctor.specialties = specialty
            doctor.save()

            return redirect('/admin-panel/doctors/?updated=true')
        except Exception as e:
            context = {
                'doctor': doctor,
                'specialties': specialties,
                'error': f'Error updating doctor: {str(e)}',
            }
            return render(request, 'admin_panel/edit_doctor.html', context)

    # GET request
    context = {
        'doctor': doctor,
        'specialties': specialties,
    }
    return render(request, 'admin_panel/edit_doctor.html', context)


@login_required_admin
def delete_doctor(request, docid):
    """Delete doctor"""
    doctor = get_object_or_404(Doctor, docid=docid)

    if request.method == 'POST':
        email = doctor.docemail.email
        doctor.delete()
        WebUser.objects.filter(email=email).delete()
        return redirect('/admin-panel/doctors/?deleted=true')

    context = {
        'doctor': doctor,
    }
    return render(request, 'admin_panel/delete_doctor.html', context)


@login_required_admin
def manage_patients(request):
    """List all patients"""
    patients = Patient.objects.select_related('pemail').all()

    context = {
        'patients': patients,
    }
    return render(request, 'admin_panel/manage_patients.html', context)


@login_required_admin
def delete_patient(request, pid):
    """Delete patient"""
    patient = get_object_or_404(Patient, pid=pid)

    if request.method == 'POST':
        email = patient.pemail.email
        patient.delete()
        WebUser.objects.filter(email=email).delete()
        return redirect('/admin-panel/patients/?deleted=true')

    context = {
        'patient': patient,
    }
    return render(request, 'admin_panel/delete_patient.html', context)


@login_required_admin
def manage_schedule(request):
    """List all sessions"""
    schedules = Schedule.objects.select_related('docid').annotate(
        appointment_count=Count('appointment')
    ).order_by('-scheduledate', '-scheduletime')

    context = {
        'schedules': schedules,
    }
    return render(request, 'admin_panel/manage_schedule.html', context)


@login_required_admin
def add_schedule(request):
    """Add new session"""
    doctors = Doctor.objects.select_related('specialties').all()

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor', '').strip()
        title = request.POST.get('title', '').strip()
        schedule_date = request.POST.get('scheduledate', '').strip()
        schedule_time = request.POST.get('scheduletime', '').strip()
        nop = request.POST.get('nop', '').strip()

        if not all([doctor_id, title, schedule_date, schedule_time, nop]):
            context = {
                'doctors': doctors,
                'error': 'All fields are required',
            }
            return render(request, 'admin_panel/add_schedule.html', context)

        try:
            doctor = Doctor.objects.get(docid=doctor_id)
            Schedule.objects.create(
                docid=doctor,
                title=title,
                scheduledate=schedule_date,
                scheduletime=schedule_time,
                nop=int(nop)
            )
            return redirect('/admin-panel/schedule/?added=true')
        except Exception as e:
            context = {
                'doctors': doctors,
                'error': f'Error creating schedule: {str(e)}',
            }
            return render(request, 'admin_panel/add_schedule.html', context)

    # GET request
    context = {
        'doctors': doctors,
    }
    return render(request, 'admin_panel/add_schedule.html', context)


@login_required_admin
def delete_schedule(request, scheduleid):
    """Delete session"""
    schedule = get_object_or_404(Schedule, scheduleid=scheduleid)

    if request.method == 'POST':
        schedule.delete()
        return redirect('/admin-panel/schedule/?deleted=true')

    appointment_count = Appointment.objects.filter(scheduleid=schedule).count()

    context = {
        'schedule': schedule,
        'appointment_count': appointment_count,
    }
    return render(request, 'admin_panel/delete_schedule.html', context)


@login_required_admin
def view_appointments(request):
    """View all appointments"""
    appointments = Appointment.objects.select_related(
        'pid',
        'pid__pemail',
        'scheduleid',
        'scheduleid__docid'
    ).order_by('-appodate')

    # Filters
    filter_date = request.GET.get('date', '')
    filter_doctor = request.GET.get('doctor', '')

    if filter_date:
        appointments = appointments.filter(appodate=filter_date)

    if filter_doctor:
        appointments = appointments.filter(scheduleid__docid__docid=filter_doctor)

    # Get all doctors for filter dropdown
    doctors = Doctor.objects.all()

    context = {
        'appointments': appointments,
        'doctors': doctors,
        'filter_date': filter_date,
        'filter_doctor': filter_doctor,
    }
    return render(request, 'admin_panel/view_appointments.html', context)
