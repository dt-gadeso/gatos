from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .form import CreateNewUser, LoginUser, CreateRole
from django.contrib import auth

def users(request):
    return render(request, 'users.html')

def signup(request):    
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CreateNewUser()
        })
    else:
        if request.POST["password"] != request.POST["confirm_password"]:
            return render(request, 'signup.html', {
                'form': CreateNewUser(),
                "error": 'La contraseña no coincide o informacion invalida'
            })
        else:
            User = auth.get_user_model()
            if User.objects.filter(username=request.POST["username"]).exists():
                return render(request, 'signup.html', { 
                    'form': CreateNewUser(),
                    'error': 'El usuario ya existe'
                })
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password"],
                    email=request.POST["email"]
                )
                user.save()
                return redirect('signin')
            except Exception as usuari:
                return render(request, 'signup.html', { 
                    'form': CreateNewUser(),
                    'error': f'Error al crear el usuario: {str(usuari)}'
                })

def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': LoginUser()
        })
    else:
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {
                'form': LoginUser(),
                'error': 'Contraseña incorrecta o usuario no existe'
            })

def signout(request):
    logout(request)
    return redirect('/')

def role(request):
    if request.method == 'GET':
        return render(request, 'role.html', {
            'form': CreateRole()
        })
    else:
        form = CreateRole(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'role.html', {
                'form': form,
                'error': 'Informacion invalida para la creacion del role'
            })
        