from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .form import CreateNewUser, LoginUser,EditUser, AssociationForm
from .models import User, Role, Member, Manager, Association, Capturador, Free
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse

class Staff(View):
    def get(self, request):
        # Controla el acceso de usuario autenticado y lista roles y asociaciones
        if request.user.is_authenticated:
            roles = Role.objects.all()
            associations = Association.objects.all()
            return render(request, 'areaStaff.html', {'roles': roles, 'associations': associations})
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


def area_staff(request):
    roles = Role.objects.all()
    users = User.objects.all()
    associations = Association.objects.all()
    return render(request, 'areaStaff.html', {'roles': roles, 'users': users, 'associations': associations})

@login_required
def assign_role(request):
    if not request.user.is_superuser:
        return redirect('areaStaff')
    roles = Role.objects.all()
    users = User.objects.all()
    associations = Association.objects.all()
    error = None

    if request.method == 'POST':
        if 'create_role' in request.POST:
            # Crear un nuevo rol
            role_name = request.POST.get('new_role_name')
            if role_name:
                if not Role.objects.filter(name=role_name).exists():
                    Role.objects.create(name=role_name)
                else:
                    error = 'Ese rol ya existe.'
            else:
                error = 'Debes ingresar un nombre para el rol.'
        
        elif 'delete_role' in request.POST:
            # Borrar rol
            delete_role_id = request.POST.get('delete_role_id')
            if delete_role_id:
                try:
                    role = get_object_or_404(Role, id=delete_role_id)
                    
                    # Verificar si hay usuarios con este rol
                    users_with_role = User.objects.filter(role=role).count()
                    
                    if users_with_role > 0:
                        error = f'No se puede borrar el rol "{role.name}" porque hay {users_with_role} usuario(s) asignado(s) a este rol'
                    else:
                        role_name = role.name
                        role.delete()
                        # Recargar roles después de borrar
                        roles = Role.objects.all()
                        return render(request, 'role.html', {
                            'roles': roles,
                            'users': users,
                            'success': f'Rol "{role_name}" eliminado exitosamente'
                        })
                        
                except Exception as e:
                    error = f'Error al eliminar rol: {str(e)}'
            else:
                error = 'Debes seleccionar un rol para borrar.'
        
        else:
            user_id = request.POST.get('user_id')
            role_id = request.POST.get('role_id')
            association_id = request.POST.get('association_id')
            print("association_id recibido:", association_id)
            if user_id and role_id:
                user = get_object_or_404(User, id=user_id)
                role = get_object_or_404(Role, id=role_id)
                association = None
                if association_id and association_id != "":
                    try:
                        association = Association.objects.get(id=int(association_id))
                    except Association.DoesNotExist:
                        association = None

                # Elimina al usuario de ambas tablas antes de asignar el nuevo rol
                Manager.objects.filter(user=user).delete()
                Member.objects.filter(user=user).delete()

                # Asigna el usuario a la tabla correspondiente según el rol
                if role.name.lower() == 'manager':
                    Manager.objects.update_or_create(
                        user=user,
                        defaults={'association': association}
                    )
                elif role.name.lower() == 'member':
                    Member.objects.update_or_create(
                        user=user,
                        defaults={'association': association}
                    )

                user.role = role
                user.save()

                print("user.association.id guardado:", user.association.id if user.association else None)
                return redirect('areaStaff')
            else:
                error = 'Debes seleccionar un usuario y un rol.'



    return render(request, 'role.html', {
        'roles': roles,
        'users': users,
        'associations': associations,
        'error': error
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

# --- Asociación fusionada aquí ---
@login_required
def association_list(request):
    associations = Association.objects.all()
    return render(request, 'association.html', {'associations': associations})

@login_required
def association_create(request):
    if not request.user.is_superuser:
        return redirect('association_list')
    if request.method == 'POST':
        form = AssociationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('association_list')
    else:
        form = AssociationForm()
    return render(request, 'asignar.html', {'form': form})


@receiver(post_save, sender=User)
def role_manager(sender, instance, **kwargs):
    # Verifica si el usuario tiene un rol y si ese rol es "manager"
    if hasattr(instance, 'role') and instance.role and instance.role.name.lower() == 'manager':
        # Crea o actualiza el registro en la tabla Manager con el user_id
        Manager.objects.update_or_create(user_id=instance.id, defaults={})
       
        
@receiver(post_save, sender=User)
def role_member(sender, instance, **kwargs):
    # Verifica si el usuario tiene un rol y si ese rol es "member"
    if hasattr(instance, 'role') and instance.role and instance.role.name.lower() == 'member':
        # Crea o actualiza el registro en la tabla Member con el user_id
        Member.objects.update_or_create(user_id=instance.id, defaults={})

@receiver(post_save, sender=User)
def role_free(sender, instance, **kwargs):
    # Verifica si el usuario tiene un rol y si ese rol es "free"
    if hasattr(instance, 'role') and instance.role and instance.role.name.lower() == 'free':
        # Crea o actualiza el registro en la tabla Free con el user_id
        Free.objects.update_or_create(user_id=instance.id, defaults={})

@receiver(post_save, sender=User)
def role_capturador(sender, instance, **kwargs):
    # Verifica si el usuario tiene un rol y si ese rol es "capturador"
    if hasattr(instance, 'role') and instance.role and instance.role.name.lower() == 'capturador':
        # Crea o actualiza el registro en la tabla Capturador con el user_id
        Capturador.objects.update_or_create(user_id=instance.id, defaults={})