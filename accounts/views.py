from django.shortcuts import render, redirect
from django.contrib import messages
from .models import WebUser, Admin
from patient.models import Patient
from doctor.models import Doctor


def index(request):
    """Landing page - no authentication required"""
    return render(request, 'index.html')


def login_view(request):
    """Login view for all user types"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            # Check if user exists
            web_user = WebUser.objects.get(email=email)
            usertype = web_user.usertype

            # Check credentials based on usertype
            if usertype == 'p':
                # Patient login
                try:
                    patient = Patient.objects.get(pemail=email, ppassword=password)
                    # Set session
                    request.session['user'] = email
                    request.session['usertype'] = 'p'
                    request.session['username'] = patient.pname
                    return redirect('/patient/')
                except Patient.DoesNotExist:
                    error = "Wrong credentials"

            elif usertype == 'd':
                # Doctor login
                try:
                    doctor = Doctor.objects.get(docemail=email, docpassword=password)
                    # Set session
                    request.session['user'] = email
                    request.session['usertype'] = 'd'
                    request.session['username'] = doctor.docname
                    return redirect('/doctor/')
                except Doctor.DoesNotExist:
                    error = "Wrong credentials"

            elif usertype == 'a':
                # Admin login
                try:
                    admin = Admin.objects.get(aemail=email, apassword=password)
                    # Set session
                    request.session['user'] = email
                    request.session['usertype'] = 'a'
                    request.session['username'] = 'Admin'
                    return redirect('/admin/')
                except Admin.DoesNotExist:
                    error = "Wrong credentials"
            else:
                error = "Invalid user type"

        except WebUser.DoesNotExist:
            error = "No account found for this email"

        # Render with error
        return render(request, 'login.html', {'error': error})

    # GET request
    return render(request, 'login.html')


def signup(request):
    """Signup step 1 - collect personal information"""
    if request.method == 'POST':
        # Get form data
        fname = request.POST.get('fname', '').strip()
        lname = request.POST.get('lname', '').strip()
        address = request.POST.get('address', '').strip()
        nic = request.POST.get('nic', '').strip()
        dob = request.POST.get('dob', '').strip()

        # Save to session
        request.session['personal'] = {
            'fname': fname,
            'lname': lname,
            'address': address,
            'nic': nic,
            'dob': dob,
        }

        # Redirect to step 2
        return redirect('/create-account/')

    # GET request
    return render(request, 'signup.html')


def create_account(request):
    """Signup step 2 - create account"""
    # Check if step 1 was completed
    if 'personal' not in request.session:
        return redirect('/signup/')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Check if email already exists
        if WebUser.objects.filter(email=email).exists():
            error = "Account already exists"
            return render(request, 'create-account.html', {'error': error})

        # Check password match
        if password != confirm_password:
            error = "Password mismatch"
            return render(request, 'create-account.html', {'error': error})

        # Get personal info from session
        personal = request.session['personal']
        fname = personal['fname']
        lname = personal['lname']
        full_name = f"{fname} {lname}"

        # Create WebUser
        web_user = WebUser.objects.create(
            email=email,
            usertype='p'
        )

        # Create Patient
        Patient.objects.create(
            pemail=web_user,
            pname=full_name,
            ppassword=password,
            paddress=personal['address'],
            pnic=personal['nic'],
            ptel=phone,
            pdob=personal['dob']
        )

        # Clear session personal data
        del request.session['personal']

        # Set login session
        request.session['user'] = email
        request.session['usertype'] = 'p'
        request.session['username'] = fname

        # Redirect to patient dashboard
        return redirect('/patient/')

    # GET request
    return render(request, 'create-account.html')


def logout_view(request):
    """Logout and clear session"""
    request.session.flush()
    return redirect('/login/')
