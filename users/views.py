from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .form import CreateNewUser, LoginUser, CreateRole
from .models import User
from django.contrib.auth.decorators import login_required

def users(request):
    if request.user.is_authenticated:
        return render(request, 'areaStaff.html')
    else:
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
            form = CreateNewUser(request.POST, request.FILES)
            if User.objects.filter(username=request.POST["username"]).exists():
                return render(request, 'signup.html', { 
                    'form': CreateNewUser(),
                    'error': 'El usuario ya existe'
                })
            try:
                if form.is_valid():
                    print("Cleaned data:", form.cleaned_data)
                    user = User(
                        username=form.cleaned_data.get('username'),
                        email=form.cleaned_data.get('email'),
                        avatar_file=form.cleaned_data.get('avatar_file'),
                        volunteer_number=form.cleaned_data.get('volunteer_number')
                    )
                    user.set_password(form.cleaned_data.get('password'))
                    user.save()
                    return redirect('signin')
                else:
                    return render(request, 'signup.html', { 
                        'form': form,
                        'error': 'Información inválida para crear el usuario'
                    })
            except Exception as e:
                return render(request, 'signup.html', { 
                    'form': CreateNewUser(),
                    'error': f'Error al crear el usuario: {str(e)}'
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

@login_required
def signout(request):
    logout(request)
    return redirect('/')

@login_required
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
        
@login_required
def view_data_user(request):
    d
        