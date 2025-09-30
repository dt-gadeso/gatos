from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .form import CreateNewUser, LoginUser,EditUser, AssociationForm
from .models import User, Role, Member, Manager, Association, TrapType
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

class Staff(View):
    def get(self, request):
        if request.user.is_authenticated:
            roles = Role.objects.all()
            associations = Association.objects.all()
            users = User.objects.all()
            return render(request, 'areaStaff.html', {
                'roles': roles,
                'associations': associations,
                'users': users
            })
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
                    casa_acogida_val = request.POST.get('casa_acogida')
                    tiene_relevo_val = request.POST.get('tiene_relevo')
                    if casa_acogida_val != 'si':
                        tiene_relevo_val = 'no'
                    es_capturador_val = form.cleaned_data.get('es_capturador')
                    trap_type_val = form.cleaned_data.get('trap_type')
                    
                    user = User(
                        username=form.cleaned_data.get('username'),
                        email=form.cleaned_data.get('email'),
                        phone=form.cleaned_data.get('phone'),
                        carnet_gatos=form.cleaned_data.get('carnet_gatos'),
                        casa_acogida=(casa_acogida_val == 'si'),
                        tiene_relevo=(tiene_relevo_val == 'si'),
                        es_capturador=(es_capturador_val == 'si'),
                        trap_type=trap_type_val if es_capturador_val == 'si' else None
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
            user.activo = True
            user.save()
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
    trap_types = TrapType.objects.all()
    selected_role_id = request.POST.get('role_id')
    selected_association_id = request.POST.get('association_id')
    error = None
    show_association = False

    if selected_role_id:
        try:
            role = Role.objects.get(id=selected_role_id)
            show_association = role.name.lower() in ['presidente/a', 'miembro']
        except Role.DoesNotExist:
            error = "Rol inválido"

    if request.method == 'POST' and 'assign_role' in request.POST:
        user_id = request.POST.get('user_id')

        if not user_id or not selected_role_id:
            error = "Debes seleccionar un usuario y un rol."
        else:
            user = get_object_or_404(User, id=user_id)
            role = get_object_or_404(Role, id=selected_role_id)
            association = None

            if show_association and selected_association_id:
                association = get_object_or_404(Association, id=selected_association_id)

            Manager.objects.filter(user=user).delete()
            Member.objects.filter(user=user).delete()

            user.es_capturador = False
            user.es_free = False
            user.trap_type = None

            if role.name.lower() == 'presidente/a':
                Manager.objects.update_or_create(user=user, defaults={'association': association})
            elif role.name.lower() == 'miembro':
                Member.objects.update_or_create(user=user, defaults={'association': association})
            elif role.name.lower() == 'capturador':
                user.es_capturador = True
                selected_trap_type = request.POST.get('trap_type')
                if selected_trap_type:
                    user.trap_type = TrapType.objects.get(id=selected_trap_type)
            elif role.name.lower() == 'free':
                user.es_free = True

            user.role = role
            user.association = association if show_association else None
            user.save()
            return redirect('areaStaff')

    return render(request, 'role.html', {
        'roles': roles,
        'users': users,
        'associations': associations,
        'trap_types': trap_types,
        'selected_role_id': int(selected_role_id) if selected_role_id else None,
        'selected_association_id': int(selected_association_id) if selected_association_id else None,
        'show_association': show_association,
        'error': error
    })

@login_required
def delete_user(request):
    if request.method == "POST":
        if not request.user.is_superuser:
            return JsonResponse({"error": "No tienes permiso para borrar usuarios"}, status=403)

        user_id = request.POST.get('user_id')
        if not user_id:
            return JsonResponse({"error": "No se especificó usuario a borrar"}, status=400)

        user_to_delete = get_object_or_404(User, id=user_id)

        if user_to_delete == request.user:
            return JsonResponse({"error": "No puedes borrar tu propia cuenta desde aquí"}, status=400)

        user_to_delete.delete()
        return JsonResponse({"message": f"Usuario {user_to_delete.username} eliminado con éxito"}, status=200)

    return JsonResponse({"error": "Método no permitido"}, status=400)


@login_required
def areaEdit(request):
    if request.method == 'GET':
        form = EditUser(instance=request.user)
        roles = Role.objects.all()
        associations = Association.objects.all()
        return render(request, 'areaEdit.html', {
            'user': request.user,
            'form': form,
            'roles': roles,
            'associations': associations
        })
    else:
        try:
            form = EditUser(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                user = request.user
                for field in ['username', 'email', 'phone', 'carnet_gatos']:
                    value = form.cleaned_data.get(field)
                    if value not in [None, '', [], {}]:
                        setattr(user, field, value)
                
                casa_acogida_val = form.cleaned_data.get('casa_acogida')
                tiene_relevo_val = form.cleaned_data.get('tiene_relevo')
                
                if casa_acogida_val is not None:
                    user.casa_acogida = (casa_acogida_val == 'si')
                
                if casa_acogida_val == 'no':
                    user.tiene_relevo = False
                elif tiene_relevo_val is not None:
                    user.tiene_relevo = (tiene_relevo_val == 'si')
                
                es_capturador_val = form.cleaned_data.get('es_capturador')
                if es_capturador_val is not None:
                    es_capturador_nuevo = (es_capturador_val == 'si')
                    user.es_capturador = es_capturador_nuevo
                    # Solo permitir tipo de trampa si es capturador
                    if not es_capturador_nuevo:
                        user.trap_type = None

                trap_type_val = form.cleaned_data.get('trap_type')
                if user.es_capturador:
                    user.trap_type = trap_type_val
                
                es_free_val = form.cleaned_data.get('es_free')
                if es_free_val is not None:
                    user.es_free = (es_free_val == 'si')
                
                association_val = form.cleaned_data.get('association')
                if association_val:
                    user.association = association_val
                else:
                    user.association = None
                
                user.save()
                return redirect('areaStaff')
            else:
                roles = Role.objects.all()
                associations = Association.objects.all()
                return render(request, 'areaEdit.html', {
                    'form': form,
                    'user': request.user,
                    'roles': roles,
                    'associations': associations,
                    'error': 'Formulario inválido'
                })
        except Exception as e:
            roles = Role.objects.all()
            associations = Association.objects.all()
            return render(request, 'areaEdit.html', {
                'form': EditUser(instance=request.user),
                'user': request.user,
                'roles': roles,
                'associations': associations,
                'error': f'Error al editar el usuario: {str(e)}'
            })

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
    if hasattr(instance, 'role') and instance.role and instance.role.name.lower() == 'presidente/a':
        Manager.objects.update_or_create(user_id=instance.id, defaults={})
       
        
@receiver(post_save, sender=User)
def role_member(sender, instance, **kwargs):
    if hasattr(instance, 'role') and instance.role and instance.role.name.lower() == 'miembro':
        Member.objects.update_or_create(user_id=instance.id, defaults={})


@require_GET
def search_users(request):
    query = request.GET.get('search', '').strip().lower()
    users = []
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).values('id', 'username', 'email')
    else:
        users = User.objects.all().values('id', 'username', 'email')
    return JsonResponse(list(users), safe=False)

@require_GET
def search_associations(request):
    query = request.GET.get('search', '').strip().lower()
    associations = []
    if query:
        associations = Association.objects.filter(
            name__icontains=query
        ).values('id', 'name')
    else:
        associations = Association.objects.all().values('id', 'name')
    return JsonResponse(list(associations), safe=False)


@login_required
@csrf_exempt
def admin_delete_user(request):
    if request.method == 'POST' and request.user.is_superuser:
        user_id = request.POST.get('user_id')
        user_to_delete = get_object_or_404(User, id=user_id)
        user_to_delete.delete()
        return JsonResponse({'message': f'Usuario {user_to_delete.username} eliminado con éxito'}, status=200)
    return JsonResponse({'error': 'No autorizado o método inválido'}, status=400)


@login_required
def user_management(request):
    """Vista para gestión simplificada de usuarios - Solo administradores"""
    if not request.user.is_superuser:
        return redirect('/')
    
    # Consulta básica sin optimizaciones complejas
    users = User.objects.all().order_by('-created_at')
    
    return render(request, 'user_management.html', {
        'users': users,
    })


@login_required
def user_edit_admin(request, user_id):
    """Vista para editar usuario - Solo administradores"""
    if not request.user.is_superuser:
        return redirect('/')
    
    user_to_edit = get_object_or_404(User, id=user_id)
    roles = Role.objects.all()
    associations = Association.objects.all()
    trap_types = TrapType.objects.all()
    
    if request.method == 'POST':
        # Actualizar datos del usuario
        user_to_edit.username = request.POST.get('username', user_to_edit.username)
        user_to_edit.email = request.POST.get('email', user_to_edit.email)
        user_to_edit.first_name = request.POST.get('first_name', '')
        user_to_edit.last_name = request.POST.get('last_name', '')
        user_to_edit.phone = request.POST.get('phone', '')
        user_to_edit.activo = request.POST.get('activo') == 'on'
        user_to_edit.casa_acogida = request.POST.get('casa_acogida') == 'on'
        user_to_edit.tiene_relevo = request.POST.get('tiene_relevo') == 'on'
        user_to_edit.es_capturador = request.POST.get('es_capturador') == 'on'
        user_to_edit.es_free = request.POST.get('es_free') == 'on'
        
        # Actualizar rol
        role_id = request.POST.get('role')
        if role_id:
            user_to_edit.role = get_object_or_404(Role, id=role_id)
        else:
            user_to_edit.role = None
            
        # Actualizar asociación
        association_id = request.POST.get('association')
        if association_id:
            user_to_edit.association = get_object_or_404(Association, id=association_id)
        else:
            user_to_edit.association = None
            
        # Actualizar tipo de trampa
        trap_type_id = request.POST.get('trap_type')
        if trap_type_id:
            user_to_edit.trap_type = get_object_or_404(TrapType, id=trap_type_id)
        else:
            user_to_edit.trap_type = None
        
        user_to_edit.save()
        
        return JsonResponse({'success': True, 'message': 'Usuario actualizado correctamente'})
    
    return render(request, 'user_edit_admin.html', {
        'user_to_edit': user_to_edit,
        'roles': roles,
        'associations': associations,
        'trap_types': trap_types
    })

