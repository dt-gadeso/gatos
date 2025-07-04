from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Municipality, Location, Zone, Council, Incident, Colony
from .form import LocationForm, MunicipalityForm, ZoneForm, CouncilForm, ColonyForm, EditIncident, IncidentForm
from django.contrib.auth.decorators import login_required

# Vista principal que muestra las ubicaciones, municipios y zonas
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

# Devuelve las ubicaciones en formato JSON para uso en el frontend
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
# Guarda una nueva ubicación, acepta datos por POST o JSON
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
# Guarda una nueva zona, acepta datos por POST o JSON
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
# Crea rápidamente una ubicación desde una petición AJAX/JSON
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

@csrf_exempt
def save_council(request):
    if request.method == 'GET':
        return render(request, 'formNewCouncil.html', {'form': CouncilForm()})

    elif request.method == 'POST':
        is_ajax = False
        try:
            if request.content_type == 'application/json':
                if not request.body:
                    return JsonResponse({'success': False, 'error': 'Request body is empty'}, status=400)
                data = json.loads(request.body)
                is_ajax = True
                files = None
            else:
                data = request.POST
                files = request.FILES

            form = CouncilForm(data, files)
            if form.is_valid():
                council = Council.objects.create(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    emergency_email=form.cleaned_data['emergency_email'],
                    emergency_phone=form.cleaned_data['emergency_phone'],
                    logo_file=form.cleaned_data['logo_file'],
                    location=form.cleaned_data['location'],
                )
                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'Guardado exitosamente'})
                return redirect('colonies')
            else:
                if is_ajax:
                    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
                return render(request, 'formNewCouncil.html', {'form': form})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            return render(request, 'formNewCouncil.html', {'form': CouncilForm(), 'error': str(e)})

    return JsonResponse({'error': 'Método no permitido'}, status=405)


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
                    colony=form.cleaned_data['colony']
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