from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .form import createnewuser, loginuser
from django.contrib import auth

def users(request):
    return render(request, 'users.html')

def signup(request):    
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': createnewuser()
        })
    else:
        if request.POST["password"] != request.POST["confirm_password"]:
            return render(request, 'signup.html', {
                'form': createnewuser(),
                "error": 'Passwords do not match or invalid data'
            })
        else:
            try:
                user = auth.get_user_model().objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password"],
                    email=request.POST["email"]
                )
                user.save()
                return redirect('signin')
            except Exception:
                return render(request, 'signup.html', { 
                    'form': createnewuser(),
                    'error': 'User already exists'
                })

def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': loginuser()
        })
    else:
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username == '' or password == '':
            return render(request, 'login.html', {
                'form': loginuser(),
                'error': 'Por favor ingrese usuario y contraseña'
            })
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {
                'form': loginuser(),
                'error': 'Contraseña incorrecta o usuario no existe'
            })

def signout(request):
    logout(request)
    return redirect('/')


