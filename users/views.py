from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def users(request):
    return render(request, 'users.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('signin')
            except Exception:
                return render(request, 'signup.html', { 
                    'form': UserCreationForm(),
                    'error': 'User already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm(),
            'error': 'Password do not match'
        })

def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
        if user is not None:
            login(request, user)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return render(request, 'login.html', {
                'form': AuthenticationForm(),
                'error': 'Por favor ingrese usuario y contraseña'
            })
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'form': AuthenticationForm(),
                'error': 'Contraseña incorrecta o usuario no existe'
            })

def signout(request):
    logout(request)
    return redirect('signin')