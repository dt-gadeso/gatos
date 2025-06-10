from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Municipality, Location, Zone
from .form import LocationForm, MunicipalityForm, ZoneForm

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
        return render(request, 'location.html', {
            'form': LocationForm()
        })
    else:
        if request.method == 'POST':
            try:
                # Handle both JSON and form data
                if request.content_type == 'application/json':
                    if not request.body:
                        return JsonResponse({'success': False, 'error': 'Request body is empty'}, status=400)
                    data = json.loads(request.body)
                    is_ajax = True
                else:
                    # Handle form data
                    data = request.POST
                    is_ajax = False
                
                print(f"Datos recibidos en save_location: {data}")
                
                # Obtener o crear municipio por defecto
                municipality_id = data.get('municipality_id')
                if municipality_id:
                    municipality = Municipality.objects.get(id=municipality_id)
                else:
                    # Usar el primer municipio o crear uno por defecto
                    municipality = Municipality.objects.first()
                    if not municipality:
                        municipality = Municipality.objects.create(name="Default Municipality")
                
                location = Location.objects.create(
                    nombre=data.get('name', 'Ubicación sin nombre'),
                    description=data.get('description', ''),
                    address=data.get('address', data.get('name', 'Dirección no especificada')),
                    latitude=data.get('latitude'),
                    longitude=data.get('longitude'),
                    municipality=municipality
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'id': location.id,
                        'message': 'Ubicación guardada exitosamente'
                    })
                else:
                    return redirect('municipality')
                
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)
            except Exception as e:
                print(f"Error en save_location: {str(e)}")
                if 'is_ajax' in locals() and is_ajax:
                    return JsonResponse({
                        'success': False,
                        'error': str(e)
                    }, status=400)
                else:
                    return render(request, 'location.html', {
                        'form': LocationForm(),
                        'error': str(e)
                    })
        
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def save_municipality(request):
    if request.method == 'GET':
        return render(request, 'formNewMunicipality.html', {
            'form': MunicipalityForm()
        })
    elif request.method == 'POST':
        try:
            # Handle both JSON and form data
            if request.content_type == 'application/json':
                if not request.body:
                    return JsonResponse({'success': False, 'error': 'Request body is empty'}, status=400)
                data = json.loads(request.body)
                is_ajax = True
            else:
                # Handle form data
                data = request.POST
                is_ajax = False
            
            name = data.get('name')
            zone_id = data.get('zone_id')
            
            if zone_id:
                zone = Zone.objects.get(id=zone_id)
            else:
                # Usar la primera zona o crear una por defecto
                zone = Zone.objects.first()
                if not zone:
                    zone = Zone.objects.create(name="Default Zone")

            if not name:
                if is_ajax:
                    return JsonResponse({'success': False, 'error': 'El nombre es requerido.'}, status=400)
                else:
                    return render(request, 'formNewMunicipality.html', {
                        'form': MunicipalityForm(),
                        'error': 'El nombre es requerido.'
                    })

            municipality = Municipality.objects.create(
                name=name,
                zone=zone
            )

            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'id': municipality.id,
                    'message': 'Municipio guardado exitosamente'
                })
            else:
                return redirect('municipality')
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            if 'is_ajax' in locals() and is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            else:
                return render(request, 'formNewMunicipality.html', {
                    'form': MunicipalityForm(),
                    'error': str(e)
                })
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def save_zone(request):
    if request.method == 'GET':
        return render(request, 'formNewZone.html', {
            'form': ZoneForm()
        })
    elif request.method == 'POST':
        try:
            # Handle both JSON and form data
            if request.content_type == 'application/json':
                if not request.body:
                    return JsonResponse({'success': False, 'error': 'Request body is empty'}, status=400)
                data = json.loads(request.body)
                is_ajax = True
            else:
                # Handle form data
                data = request.POST
                is_ajax = False
            
            name = data.get('name')

            if not name:
                if is_ajax:
                    return JsonResponse({'success': False, 'error': 'Nombre es requerido.'}, status=400)
                else:
                    return render(request, 'formNewZone.html', {
                        'form': ZoneForm(),
                        'error': 'Nombre es requerido.'
                    })

            zone = Zone.objects.create(
                name=name,
            )

            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'id': zone.id,
                    'message': 'Zona guardada exitosamente'
                })
            else:
                return redirect('municipality')
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            if 'is_ajax' in locals() and is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            else:
                return render(request, 'formNewZone.html', {
                    'form': ZoneForm(),
                    'error': str(e)
                })
    else:
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

def add_popup(request):
    municipalities = Municipality.objects.all()
    
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save()
            return redirect('municipality')
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
            return redirect('municipality')
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
def delete_popup(request, location_id):
    if request.method == 'POST':
        try:
            location = get_object_or_404(Location, id=location_id)
            location.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)
