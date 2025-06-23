from django import forms
from colonies.models import Municipality, Location, Council
from users.models import User
from cats.models import Cat
from .models import VetCenter, Agreement, VetService, Visit, VisitService

class VetCenterForm(forms.Form):
    name = forms.CharField(
        label='Nombre',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del centro'})
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    phone = forms.CharField(
        label='Teléfono',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 600123123'})
    )
    logo_file = forms.CharField(
        label='Archivo del logo',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ruta o URL del logo'})
    )
    location = forms.ModelChoiceField(
        label='Ubicación',
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class AgreementForm(forms.Form):
    council = forms.ModelChoiceField(
        label='Ayuntamiento',
        queryset=Council.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    vet_center = forms.ModelChoiceField(
        label='Centro veterinario',
        queryset=VetCenter.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    week_days = forms.IntegerField(
        label='Días por semana',
        min_value=0,
        max_value=7,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    week_cats = forms.IntegerField(
        label='Gatos por semana',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class VetServiceForm(forms.Form):
    name = forms.CharField(
        label='Nombre del servicio',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

class VisitForm(forms.Form):
    cat = forms.ModelChoiceField(
        label='Gato',
        queryset=Cat.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    vet_center = forms.ModelChoiceField(
        label='Centro veterinario',
        queryset=VetCenter.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    price = forms.DecimalField(
        label='Precio',
        max_digits=10,
        decimal_places=2,
        min_value=0.00,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    report_file = forms.CharField(
        label='Archivo del informe',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    bill_file = forms.CharField(
        label='Archivo de la factura',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    user = forms.ModelChoiceField(
        label='Usuario',
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    visit_date = forms.DateField(
        label='Fecha de la visita',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

class VisitServiceForm(forms.Form):
    visit = forms.ModelChoiceField(
        label='Visita',
        queryset=Visit.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    vet_service = forms.ModelChoiceField(
        label='Servicio veterinario',
        queryset=VetService.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
