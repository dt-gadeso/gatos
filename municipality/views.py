from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Municipality, Location, Zone

def municipality_view(request):
    """Vista principal para mostrar el mapa con todas las ubicaciones"""
    locations = Location.objects.filter(latitude__isnull=False, longitude__isnull=False)
    municipalities = Municipality.objects.all()
    
    context = {
        'locations': locations,
        'municipalities': municipalities,
    }
    return render(request, 'municipality.html', context)

def get_locations_json(request):
    """API endpoint para obtener todas las ubicaciones en formato JSON"""
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
    """API endpoint para guardar nuevas ubicaciones"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
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
            
            return JsonResponse({
                'success': True,
                'id': location.id,
                'message': 'Ubicación guardada exitosamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def location_detail(request, location_id):
    """Vista para mostrar detalles de una ubicación específica"""
    location = get_object_or_404(Location, id=location_id)
    
    context = {
        'location': location,
    }
    return render(request, 'location.html', context)

@login_required
def newLocation(request):    
    if request.method == 'GET':
        return render(request, 'location.html', {
            'form': CreateCat(user=request.user)
        })
    else:
        form = CreateCat(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            try:
                print("Cleaned data:", form.cleaned_data)
                cat = Cat(
                    catname=form.cleaned_data.get('catname'),
                    photo_file=form.cleaned_data.get('photo_file'),
                    chip=form.cleaned_data.get('chip'),
                    birthday=form.cleaned_data.get('birthday'),
                    sex=form.cleaned_data.get('sex'),
                    sterilized=form.cleaned_data.get('sterilized') == 'True',
                    dead=form.cleaned_data.get('dead') == 'True',
                    colony=form.cleaned_data.get('colony').id if form.cleaned_data.get('colony') else None,
                    user=request.user
                )
                cat.save()
                return redirect('cats')  
            except Exception as e:
                print("Error:", e)
                return render(request, 'location.html.html', { 
                    'form': form,
                    'error': f'Error al crear el gato: {str(e)}'
                })
        else:
            print("Form errors:", form.errors)
            return render(request, 'location.html.html', {
                'form': form,
                'error': 'Formulario inválido'
            })
        