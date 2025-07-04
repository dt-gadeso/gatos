from django.shortcuts import render, redirect
from .form import VetCenterForm, AgreementForm, VetServiceForm, VisitForm, VisitServiceForm
from .models import VetCenter, VetService, Agreement
from colonies.models import Location

# Create your views here.
def veterinarian(request):
    locations = Location.objects.all()
    vet_centers = VetCenter.objects.all()
    return render(request, 'veterinarian.html', {
        'locations': locations,
        'vet_centers': vet_centers
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

def vetcenter_form_view(request):
    if request.method == 'GET':
        form = VetCenterForm()
        return render(request, 'formNewVetCenter.html', {'form': form})
    else:
        form = VetCenterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('veterinarian')
        else:
            return render(request, 'formNewVetCenter.html', {'form': form, 'error': 'Formulario inválido'})

def agreement_form_view(request):
    if request.method == 'GET':
        form = AgreementForm()
        return render(request, 'formNewAgreement.html', {'form': form})
    else:
        form = AgreementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('veterinarian')
        else:
            return render(request, 'formNewAgreement.html', {'form': form, 'error': 'Formulario inválido'})

def vetservice_form_view(request):
    if request.method == 'GET':
        form = VetServiceForm()
        return render(request, 'formNewVetService.html', {'form': form})
    else:
        form = VetServiceForm(request.POST)
        if form.is_valid():
            VetService.objects.create(**form.cleaned_data)
            return redirect('veterinarian')
        else:
            return render(request, 'formNewVetService.html', {'form': form, 'error': 'Formulario inválido'})

def visit_form_view(request):
    if request.method == 'GET':
        form = VisitForm()
        return render(request, 'formNewVisit.html', {'form': form})
    else:
        form = VisitForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                visit = form.save()
                print(f"Visit saved successfully with ID: {visit.id}")
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

def visitservice_form_view(request):
    if request.method == 'GET':
        form = VisitServiceForm()
        return render(request, 'formNewVisitService.html', {'form': form})
    else:
        form = VisitServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('veterinarian')
        else:
            return render(request, 'formNewVisitService.html', {'form': form, 'error': 'Formulario inválido'})