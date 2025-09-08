from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import VetCenterForm, VisitForm
from .models import VetCenter, Visit
from colonies.models import Location, Relief, Incident

def veterinarian(request):
    locations = Location.objects.all()
    
    if request.user.is_authenticated and hasattr(request.user, 'association') and request.user.association:
        vet_centers = VetCenter.objects.all()
        visits = Visit.objects.filter(user__association=request.user.association)
    else:
        vet_centers = VetCenter.objects.all()
        visits = Visit.objects.all()
    
    return render(request, 'veterinarian.html', {
        'locations': locations,
        'vet_centers': vet_centers,
        'visits': visits,
        'user_association': request.user.association if request.user.is_authenticated and hasattr(request.user, 'association') else None
    })

def search_vet_centers(request):
    filters = {}

    name = request.GET.get('name')
    location_id = request.GET.get('location')
    email = request.GET.get('email')

    if name:
        filters['name__icontains'] = name
    if location_id:
        filters['location__id'] = location_id
    if email:
        filters['email__icontains'] = email

    vet_centers = VetCenter.objects.filter(**filters)
    locations = Location.objects.all()

    context = {
        'vet_centers': vet_centers,
        'query': name or '',
        'location_id': location_id or '',
        'email': email or '',
        'locations': locations
    }

    return render(request, 'vet_search_result.html', context)

@login_required
def tablon(request):
    # Importamos los modelos necesarios de colonies
    from colonies.models import Relief, Incident
    
    # Obtenemos los avisos ordenados por fecha de inicio
    reliefs = Relief.objects.all().order_by('-start_date')
    
    # Obtenemos las incidencias ordenadas por fecha de reporte
    incidents = Incident.objects.all().order_by('-reported_at')
    
    # Comprobamos si hay incidencias
    print(f"Número de incidencias encontradas: {incidents.count()}")
    print(f"Usuario es staff: {request.user.is_staff}")
    print(f"Usuario es superuser: {request.user.is_superuser}")
    
    return render(request, 'tablon.html', {
        'reliefs': reliefs,
        'incidents': incidents,
        'user': request.user  # Agregamos explícitamente el usuario al contexto
    })


@login_required
def vetcenter_form_view(request):
    if request.method == 'GET':
        form = VetCenterForm(user=request.user if request.user.is_authenticated else None)
        return render(request, 'formNewVetCenter.html', {'form': form})
    else:
        form = VetCenterForm(request.POST, request.FILES, user=request.user if request.user.is_authenticated else None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Centro veterinario creado exitosamente.')
            return redirect('veterinarian')
        else:
            return render(request, 'formNewVetCenter.html', {'form': form, 'error': 'Formulario inválido'})

# Esta función fue eliminada por ser parte de la funcionalidad de ayuntamientos

@login_required
def visit_form_view(request):
    if request.method == 'GET':
        form = VisitForm(user=request.user if request.user.is_authenticated else None)
        return render(request, 'formNewVisit.html', {'form': form})
    else:
        form = VisitForm(request.POST, request.FILES, user=request.user if request.user.is_authenticated else None)
        
        if form.is_valid():
            try:
                visit = form.save()
                
                if not visit.cat_survived:
                    cat = visit.cat
                    cat.dead = True
                    cat.save()
                    print(f"Cat {cat.catname} marked as dead")
                
                print(f"Visit saved successfully with ID: {visit.id}")
                messages.success(request, 'Visita registrada exitosamente.')
                return redirect('veterinarian')
            except Exception as e:
                print(f"Error saving visit: {e}")
                return render(request, 'formNewVisit.html', {
                    'form': form, 
                    'error': f'Error al guardar la visita: {str(e)}'
                })
        else:
            print(f"Form errors: {form.errors}")
            print(f"Form non-field errors: {form.non_field_errors()}")
            return render(request, 'formNewVisit.html', {
                'form': form, 
                'error': 'Formulario inválido. Por favor, revise los errores.',
                'form_errors': form.errors
            })

@login_required
def visits_list_view(request):
    if hasattr(request.user, 'association') and request.user.association:
        visits = Visit.objects.filter(
            user__association=request.user.association
        ).select_related('cat', 'vet_center', 'user').order_by('-created_at')
    else:
        visits = Visit.objects.all().select_related('cat', 'vet_center', 'user').order_by('-created_at')
    
    return render(request, 'visits_list.html', {
        'visits': visits,
        'user_association': request.user.association if hasattr(request.user, 'association') else None
    })

# Esta función fue eliminada por ser parte de la funcionalidad de ayuntamientos