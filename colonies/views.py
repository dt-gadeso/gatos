from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Municipality, Location, Zone, Council
from .form import LocationForm, MunicipalityForm, ZoneForm, CouncilForm, ColonyForm

# Vista principal que muestra las ubicaciones, municipios y zonas
def municipality_view(request):
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


@csrf_exempt
# Guarda un nuevo municipio, acepta datos por POST o JSON
def save_municipality(request):
    if request.method == 'GET':
        return render(request, 'formNewMunicipality.html', {'form': MunicipalityForm()})

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
            zone_id = data.get('zone_id')

            if not name:
                msg = 'El nombre es requerido.'
                if is_ajax:
                    return JsonResponse({'success': False, 'error': msg}, status=400)
                return render(request, 'formNewMunicipality.html', {'form': MunicipalityForm(), 'error': msg})

            if zone_id:
                try:
                    zone = Zone.objects.get(id=zone_id)
                except Zone.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Zona no encontrada'}, status=404)
            else:
                zone = Zone.objects.first()
                if not zone:
                    zone = Zone.objects.create(name="Default Zone")

            municipality = Municipality.objects.create(name=name, zone=zone)

            if is_ajax:
                return JsonResponse({'success': True, 'id': municipality.id, 'message': 'Municipio guardado exitosamente'})
            return redirect('colonies')

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Formato JSON inválido'}, status=400)
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


def add_popup(request):
    municipalities = Municipality.objects.all()
    
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save()
            return redirect('colonies')
    else:
        form = LocationForm()
    
    context = {
        'form': form,
        'municipalities': municipalities,
        'is_edit': False
    }
    return render(request, 'add_popup.html', context)

def edit_popup(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    municipalities = Municipality.objects.all()
    
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('colonies')
    else:
        form = LocationForm(instance=location)
    
    context = {
        'form': form,
        'municipalities': municipalities,
        'is_edit': True,
        'location': location
    }
    return render(request, 'add_popup.html', context)

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