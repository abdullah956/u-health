from django.shortcuts import redirect
from functools import wraps


def login_required_patient(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session or request.session.get('usertype') != 'p':
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_required_doctor(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session or request.session.get('usertype') != 'd':
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_required_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session or request.session.get('usertype') != 'a':
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper
