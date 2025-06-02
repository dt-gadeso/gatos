from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .form import CreateNewUser, LoginUser, CreateRole, EditUser, AssignedRole
from .models import User, Role
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

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
def giveRole(request):
    if request.method == 'GET':
        roles = Role.objects.all()
        return render(request, 'areaStaff.html', {
            'form': AssignedRole(),
            'roles': roles
        })
    else:
        form = AssignedRole(request.POST)
        roles = Role.objects.all()
        if form.is_valid():
            form.save()
            return redirect('giveRole')
        else:
            return render(request, 'areaStaff.html', {
                'form': form,
                'roles': roles,
                'error': 'Información inválida para la creación del rol'
            })

@login_required
def AssignedRole(request, role_id=None):
    roles = Role.objects.all()
    users = User.objects.all()
    if request.method == 'GET':
        return render(request, 'areaStaff.html', {
            'form': AssignedRole(),
            'roles': roles,
            'users': users
        })
    else:
        if role_id:
            # Assign user to role
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            role = get_object_or_404(Role, id=role_id)
            user.role = role
            user.save()
            return redirect('giveRole')
        else:
            form = AssignedRole(request.POST)
            if form.is_valid():
                form.save()
                return redirect('giveRole')
            else:
                return render(request, 'areaStaff.html', {
                    'form': form,
                    'roles': roles,
                    'users': users,
                    'error': 'Información inválida para la creación del rol'
                })


@login_required
def delete_user(request):
    if request.method == "POST":
        request.user.delete()
        return JsonResponse({"message": "Cuenta eliminada con éxito"}, status=200)
    return JsonResponse({"error": "Método no permitido"}, status=400)

@login_required
def areaEdit(request):
    if request.method == 'GET':
        form = EditUser()
        return render(request, 'areaEdit.html', {
            'user': request.user,
            'form': form
        })
    else:
        try:
            form = EditUser(request.POST, request.FILES)
            if form.is_valid():
                user = request.user
                # Solo actualiza los campos que el usuario llenó
                for field, value in form.cleaned_data.items():
                    if value not in [None, '', [], {}]:
                        setattr(user, field, value)
                user.save()
                return redirect('areaStaff')
            else:
                return render(request, 'areaEdit.html', {
                    'form': form,
                    'user': request.user,
                    'error': 'Formulario inválido'
                })
        except Exception as e:
            return render(request, 'areaEdit.html', {
                'form': EditUser(),
                'user': request.user,
                'error': f'Error al editar el usuario: {str(e)}'
            })