from django.shortcuts import render, redirect
from .form import VetCenterForm, AgreementForm, VetServiceForm, VisitForm, VisitServiceForm
from .models import VetCenter, VetService, Visit, VisitService, Agreement

# Create your views here.
def veterinarian(request):
    return render(request, 'veterinarian.html')

def vetcenter_form_view(request):
    if request.method == 'GET':
        form = VetCenterForm()
        return render(request, 'formNewVetCenter.html', {'form': form})
    else:
        form = VetCenterForm(request.POST)
        if form.is_valid():
            # Aquí deberías guardar el modelo VetCenter
            # Ejemplo:
            VetCenter.objects.create(**form.cleaned_data)
            return redirect('veterinarian')
        else:
            return render(request, 'formNewVetCenter.html', {'form': form, 'error': 'Formulario inválido'})

def agreement_form_view(request):
    if request.method == 'GET':
        form = AgreementForm()
        return render(request, 'formNewAgreement.html', {'form': form})
    else:
        form = AgreementForm(request.POST)
        if form.is_valid():
            Agreement.objects.create(**form.cleaned_data)
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
        form = VisitForm(request.POST)
        if form.is_valid():
            Visit.objects.create(**form.cleaned_data)
            return redirect('veterinarian')
        else:
            return render(request, 'formNewVisit.html', {'form': form, 'error': 'Formulario inválido'})

def visitservice_form_view(request):
    if request.method == 'GET':
        form = VisitServiceForm()
        return render(request, 'formNewVisitService.html', {'form': form})
    else:
        form = VisitServiceForm(request.POST)
        if form.is_valid():
            VisitService.objects.create(**form.cleaned_data)
            return redirect('veterinarian')
        else:
            return render(request, 'formNewVisitService.html', {'form': form, 'error': 'Formulario inválido'})