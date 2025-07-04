from django import forms
from colonies.models import Municipality, Location, Council
from users.models import User
from cats.models import Cat
from .models import VetCenter, Agreement, VetService, Visit, VisitService
from decimal import Decimal

class VetCenterForm(forms.ModelForm):
    class Meta:
        model = VetCenter
        fields = ['name', 'email', 'phone', 'logo_file', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del centro'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 600123123'}),
            'logo_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'location': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'name': 'Nombre',
            'email': 'Correo electrónico',
            'phone': 'Teléfono',
            'logo_file': 'Archivo del logo',
            'location': 'Ubicación'
        }

class AgreementForm(forms.ModelForm):
    class Meta:
        model = Agreement
        fields = ['council', 'vet_center', 'week_days', 'week_cats', 'agreement_file']
        widgets = {
            'council': forms.Select(attrs={'class': 'form-control'}),
            'vet_center': forms.Select(attrs={'class': 'form-control'}),
            'week_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'week_cats': forms.NumberInput(attrs={'class': 'form-control'}),
            'agreement_file': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'council': 'Ayuntamiento',
            'vet_center': 'Centro veterinario',
            'week_days': 'Días por semana',
            'week_cats': 'Gatos por semana',
            'agreement_file': 'Archivo del acuerdo'
        }

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

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['cat', 'vet_center', 'price', 'report_file', 'bill_file', 'user', 'follow_up', 'start_date', 'end_date']
        widgets = {
            'cat': forms.Select(attrs={'class': 'form-control'}),
            'vet_center': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'report_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bill_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'follow_up': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
        labels = {
            'cat': 'Gato',
            'vet_center': 'Centro veterinario',
            'price': 'Precio',
            'report_file': 'Archivo del informe (opcional)',
            'bill_file': 'Archivo de la factura (opcional)',
            'user': 'Usuario',
            'follow_up': 'Seguimiento',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de fin'
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        price = cleaned_data.get('price')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        if price is not None and price < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")

        return cleaned_data

class VisitServiceForm(forms.ModelForm):
    class Meta:
        model = VisitService
        fields = ['visit', 'vet_service']
        widgets = {
            'visit': forms.Select(attrs={'class': 'form-control'}),
            'vet_service': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'visit': 'Visita',
            'vet_service': 'Servicio veterinario'
        }
