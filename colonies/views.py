from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Municipality, Location, Zone, Incident, Colony, Relief
from .form import LocationForm, MunicipalityForm, ZoneForm, ColonyForm, EditIncident, IncidentForm, ReliefForm, EditReliefForm
from django.contrib.auth.decorators import login_required
from django.views.defaults import page_not_found
from django.views.decorators.csrf import csrf_exempt

def mi_error_404(request, exception):
    path = request.path

    if path.startswith('/colonies/municipality'):
        return render(request, 'municipality.html', status=404)
    elif path.startswith('/colonies/formularios_multiples'):
        return render(request, 'formularios_multiples.html', status=404)
    elif path.startswith('/colonies/formNewIncident'):
        return render(request, 'formNewIncident.html', status=404)
    elif path.startswith('/colonies/incident_search_result'):
        return render(request, 'incident_search_result.html', status=404)
    elif path.startswith('/colonies/formEditIncident'):
        return render(request, 'formEditIncident.html', status=404)
    else:
        return render(request, 'municipality.html', status=404)

def colonies_view(request):
    locations = Location.objects.filter(latitude__isnull=False, longitude__isnull=False)
    municipalities = Municipality.objects.all()
    zones = Zone.objects.all()
    
    context = {
        'locations': locations,
        'municipalities': municipalities,
        'zones': zones,
    }
    return render(request, 'municipality.html', context)

def get_locations_json(request):
    locations = Location.objects.filter(latitude__isnull=False, longitude__isnull=False)
    
    locations_data = []
    for location in locations:
        locations_data.append({
            'id': location.id,
            'name': location.nombre or location.address,
            'description': location.description or '',
            'address': location.address,
            'latitude': float(location.latitude),
            'longitude': float(location.longitude),
            'municipality': location.municipality.name,
            'municipality_id': location.municipality.id,
        })
    
    return JsonResponse({'locations': locations_data})


@csrf_exempt
def save_location(request):
    if request.method == 'GET':
        return render(request, 'location.html', {'form': LocationForm()})

    elif request.method == 'POST':
        is_ajax = False
        try:
            if request.content_type == 'application/json':
                if not request.body:
                    return JsonResponse({'success': False, 'error': 'Request body is empty'}, status=400)
                data = json.loads(request.body)
                is_ajax = True
            else:
                data = request.POST
            
            print(f"Datos recibidos en save_location: {data}")

            municipality_id = data.get('municipality_id')
            municipality = None
            if municipality_id:
                try:
                    municipality = Municipality.objects.get(id=municipality_id)
                except Municipality.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Municipio no encontrado'}, status=404)
            else:
                municipality = Municipality.objects.first()
                if not municipality:
                    municipality = Municipality.objects.create(name="Default Municipality")

            location = Location.objects.create(
                nombre=data.get('name') or data.get('nombre') or 'Ubicación sin nombre',
                description=data.get('description', ''),
                address=data.get('address', data.get('name', 'Dirección no especificada')),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                municipality=municipality
            )

            if is_ajax:
                return JsonResponse({'success': True, 'id': location.id, 'message': 'Ubicación guardada exitosamente'})
            else:
                return redirect('colonies')

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            print(f"Error en save_location: {str(e)}")
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            else:
                return render(request, 'location.html', {
                    'form': LocationForm(),
                    'error': str(e)
                })

    return JsonResponse({'error': 'Método no permitido'}, status=405)


def save_municipality(request):
    if request.method == 'GET':
        return render(request, 'formNewMunicipality.html', {'form': MunicipalityForm()})

    elif request.method == 'POST':
        is_ajax = request.content_type == 'application/json'
        try:
            if is_ajax:
                data = json.loads(request.body)
                form = MunicipalityForm(data)
            else:
                form = MunicipalityForm(request.POST)

            if form.is_valid():
                municipality = form.save()
                if is_ajax:
                    return JsonResponse({'success': True, 'id': municipality.id, 'message': 'Municipio guardado exitosamente'})
                return redirect('colonies')
            else:
                if is_ajax:
                    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
                return render(request, 'formNewMunicipality.html', {'form': form})

        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            return render(request, 'formNewMunicipality.html', {'form': MunicipalityForm(), 'error': str(e)})

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def save_zone(request):
    if request.method == 'GET':
        return render(request, 'formNewZone.html', {'form': ZoneForm()})

    elif request.method == 'POST':
        is_ajax = False
        try:
            if request.content_type == 'application/json':
                if not request.body:
                    return JsonResponse({'success': False, 'error': 'Request body is empty'}, status=400)
                data = json.loads(request.body)
                is_ajax = True
            else:
                data = request.POST

            name = data.get('name')
            if not name:
                msg = 'Nombre es requerido.'
                if is_ajax:
                    return JsonResponse({'success': False, 'error': msg}, status=400)
                return render(request, 'formNewZone.html', {'form': ZoneForm(), 'error': msg})

            zone = Zone.objects.create(name=name)

            if is_ajax:
                return JsonResponse({'success': True, 'id': zone.id, 'message': 'Zona guardada exitosamente'})
            return redirect('colonies')

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            return render(request, 'formNewZone.html', {'form': ZoneForm(), 'error': str(e)})

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def create_quick_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            municipality = Municipality.objects.get(id=data.get('municipality_id'))
            
            location = Location.objects.create(
                address=data.get('address'),
                municipality=municipality,
                latitude=data.get('latitude'),
                longitude=data.get('longitude')
            )
            
            return JsonResponse({
                'success': True,
                'location_id': location.id,
                'location_name': str(location),
                'message': 'Ubicación creada exitosamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def location_detail(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    
    context = {
        'location': location,
    }
    return render(request, 'location.html', context)

def new_colony(request):
    if request.method == 'GET':
        form = ColonyForm()
        return render(request, 'formNewColony.html', {'form': form})
    elif request.method == 'POST':
        form = ColonyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('colonies')
        return render(request, 'formNewColony.html', {'form': form})

@csrf_exempt
def save_incident(request):
    if request.method == 'GET':
        return render(request, 'formNewIncident.html', {'form': IncidentForm()})

    elif request.method == 'POST':
        is_ajax = False
        try:
            if request.content_type == 'application/json':
                if not request.body:
                    return JsonResponse({'success': False, 'error': 'Request body is empty'}, status=400)
                data = json.loads(request.body)
                is_ajax = True
                form = IncidentForm(data)
            else:
                form = IncidentForm(request.POST)

            if form.is_valid():
                incident = Incident.objects.create(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    is_resolved=form.cleaned_data['is_resolved'],
                    resolution=form.cleaned_data['resolution'],
                    start_date=form.cleaned_data['start_date'],
                    end_date=form.cleaned_data['end_date'],
                    colony=form.cleaned_data['colony'],
                    cat=form.cleaned_data['cat']
                )
                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'Incidencia guardada exitosamente', 'id': incident.id})
                return redirect('colonies')
            else:
                if is_ajax:
                    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
                return render(request, 'formNewIncident.html', {'form': form})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            return render(request, 'formNewIncident.html', {
                'form': IncidentForm(),
                'error': str(e)
            })

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def editIncident(request, incident_id):
    incident = get_object_or_404(Incident, id=incident_id)

    if request.method == 'GET':
        form = EditIncident(instance=incident)
        return render(request, 'formEditIncident.html', {
            'form': form,
            'incident': incident
        })
    else:
        form = EditIncident(request.POST, instance=incident)
        if form.is_valid():
            try:
                form.save()
                return redirect('colonies')
            except Exception as e:
                return render(request, 'formEditIncident.html', {
                    'form': form,
                    'incident': incident,
                    'error': f'Error al guardar la incidencia: {str(e)}'
                })
        else:
            return render(request, 'formEditIncident.html', {
                'form': form,
                'incident': incident,
                'error': 'Formulario inválido'
            })
        
@login_required
def searchIncidents(request):
    filters = {}
    colony_id = request.GET.get('colony')
    is_resolved = request.GET.get('is_resolved')

    if colony_id:
        filters['colony__id'] = colony_id
    if is_resolved in ['true', 'false']:
        filters['is_resolved'] = is_resolved == 'true'

    incidents = Incident.objects.filter(**filters).order_by('-reported_at')
    colonies = Colony.objects.all()

    context = {
        'incidents': incidents,
        'colony_id': colony_id or '',
        'is_resolved': is_resolved or '',
        'colonies': colonies
    }

    return render(request, 'incident_search_result.html', context)

@login_required
def multi_form_view(request):
    colony_form = ColonyForm()
    municipality_form = MunicipalityForm()
    zone_form = ZoneForm()
    location_form = LocationForm()
    
    success_message = None
    error_message = None

    if request.method == 'POST':
        try:

            if 'submit_colony' in request.POST:
                colony_form = ColonyForm(request.POST, request.FILES)
                if colony_form.is_valid():
                    colony_form.save()
                    success_message = "Colonia guardada exitosamente"
                    colony_form = ColonyForm()  # Reset form after success
                else:
                    error_message = "Error al guardar la colonia. Por favor revisa los campos."

            elif 'submit_municipality' in request.POST:
                municipality_form = MunicipalityForm(request.POST)
                if municipality_form.is_valid():
                    municipality_form.save()
                    success_message = "Municipio guardado exitosamente"
                    municipality_form = MunicipalityForm()  # Reset form after success
                else:
                    error_message = "Error al guardar el municipio. Por favor revisa los campos."

            elif 'submit_zone' in request.POST:
                zone_form = ZoneForm(request.POST)
                if zone_form.is_valid():
                    Zone.objects.create(
                        name=zone_form.cleaned_data['name']
                    )
                    success_message = "Zona guardada exitosamente"
                    zone_form = ZoneForm()  # Reset form after success
                else:
                    error_message = "Error al guardar la zona. Por favor revisa los campos."

            elif 'submit_location' in request.POST:
                location_form = LocationForm(request.POST, request.FILES)
                if location_form.is_valid():
                    Location.objects.create(
                        nombre=location_form.cleaned_data.get('nombre') or 'Ubicación sin nombre',
                        address=location_form.cleaned_data['address'],
                        description=location_form.cleaned_data.get('description', ''),
                        municipality=location_form.cleaned_data['municipality'],
                        latitude=location_form.cleaned_data.get('latitude'),
                        longitude=location_form.cleaned_data.get('longitude'),
                    )
                    success_message = "Ubicación guardada exitosamente"
                    location_form = LocationForm()  # Reset form after success
                else:
                    error_message = "Error al guardar la ubicación. Por favor revisa los campos."
                    
        except Exception as e:
            error_message = f"Error inesperado: {str(e)}"

    return render(request, 'formularios_multiples.html', {
        'colony_form': colony_form,
        'municipality_form': municipality_form,
        'zone_form': zone_form,
        'location_form': location_form,
        'success_message': success_message,
        'error_message': error_message,
    })

@csrf_exempt
def save_relief(request):
    if request.method == 'GET':
        return render(request, 'formNewRelief.html', {'form': ReliefForm()})

    elif request.method == 'POST':
        is_ajax = False
        try:
            if request.content_type == 'application/json':
                if not request.body:
                    return JsonResponse({'success': False, 'error': 'El cuerpo de la petición está vacío'}, status=400)
                data = json.loads(request.body)
                is_ajax = True
                form = ReliefForm(data)
            else:
                form = ReliefForm(request.POST)

            if form.is_valid():
                relief = Relief.objects.create(
                    description=form.cleaned_data['description'],
                    start_date=form.cleaned_data['start_date'],
                    end_date=form.cleaned_data['end_date']
                )
                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'Alivio guardado exitosamente', 'id': relief.id})
                return redirect('colonies')

            else:
                if is_ajax:
                    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
                return render(request, 'formNewRelief.html', {'form': form})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            return render(request, 'formNewRelief.html', {
                'form': ReliefForm(),
                'error': str(e)
            })

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def editRelief(request, relief_id):
    relief = get_object_or_404(Relief, id=relief_id)

    if request.method == 'GET':
        form = EditReliefForm(instance=relief)
        return render(request, 'formEditRelief.html', {
            'form': form,
            'relief': relief
        })

    else:
        form = EditReliefForm(request.POST, instance=relief)
        if form.is_valid():
            try:
                form.save()
                return redirect('colonies')
            except Exception as e:
                return render(request, 'formEditRelief.html', {
                    'form': form,
                    'relief': relief,
                    'error': f'Error al guardar el alivio: {str(e)}'
                })
        else:
            return render(request, 'formEditRelief.html', {
                'form': form,
                'relief': relief,
                'error': 'Formulario inválido'
            })

@login_required
def searchReliefs(request):
    filters = {}
    description = request.GET.get('description')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if description:
        filters['description__icontains'] = description
    if start_date:
        filters['start_date__gte'] = start_date
    if end_date:
        filters['end_date__lte'] = end_date

    reliefs = Relief.objects.filter(**filters).order_by('-start_date')

    context = {
        'reliefs': reliefs,
        'filters': {
            'description': description or '',
            'start_date': start_date or '',
            'end_date': end_date or ''
        }
    }

    return render(request, 'relief_search_result.html', context)

@login_required
def duplicateRelief(request, relief_id):
    if request.method == 'POST':
        try:
            original_relief = get_object_or_404(Relief, id=relief_id)
            
            # Crear una copia del relevo
            new_relief = Relief.objects.create(
                description=f"Copia de: {original_relief.description}",
                start_date=original_relief.start_date,
                end_date=original_relief.end_date
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Relevo duplicado exitosamente',
                'new_id': new_relief.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': str(e)
            })
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def deleteRelief(request, relief_id):
    if request.method == 'DELETE':
        try:
            relief = get_object_or_404(Relief, id=relief_id)
            relief.delete()
            
            return JsonResponse({
                'success': True, 
                'message': 'Relevo eliminado exitosamente'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': str(e)
            })
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

