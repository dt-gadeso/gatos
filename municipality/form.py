from django import forms
from .models import Location, Municipality, Zone

class NewLocation(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['nombre', 'address', 'description', 'municipality', 'latitude', 'longitude']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del lugar'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del lugar'
            }),
            'municipality': forms.Select(attrs={
                'class': 'form-control'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Latitud'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Longitud'
            }),
        }
        labels = {
            'nombre': 'Nombre del lugar',
            'address': 'Dirección',
            'description': 'Descripción',
            'municipality': 'Municipio',
            'latitude': 'Latitud',
            'longitude': 'Longitud',
        }




class LocationForm(forms.Form):
    address = forms.CharField(
        label='Dirección',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la dirección'})
    )
    
    municipality = forms.ModelChoiceField(
        label='Municipio',
        queryset=Municipality.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    nombre = forms.CharField(
        label='Nombre del lugar',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'})
    )

    description = forms.CharField(
        label='Descripción',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción', 'rows': 3})
    )

    latitude = forms.DecimalField(
        label='Latitud',
        max_digits=10,
        decimal_places=8,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la latitud'})
    )

    longitude = forms.DecimalField(
        label='Longitud',
        max_digits=11,
        decimal_places=8,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la longitud'})
    )

class MunicipalityForm(forms.Form):
    name = forms.CharField(
        label='Nombre del municipio',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del municipio'})
    )
    
    zone = forms.ModelChoiceField(
        label='Zona',
        queryset=Zone.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ZoneForm(forms.Form):
    name = forms.CharField(
        label='Nombre de la zona',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la zona'})
    )

class CouncilForm(forms.Form):
    name = forms.CharField(
        label='Nombre',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del consejo'})
    )
    
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el correo'})
    )
    
    phone = forms.CharField(
        label='Teléfono',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono'})
    )

    emergency_email = forms.EmailField(
        label='Correo de emergencia',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el correo de emergencia'})
    )

    emergency_phone = forms.CharField(
        label='Teléfono de emergencia',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono de emergencia'})
    )

    logo_file = forms.ImageField(
        label='Logo',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

    location = forms.ModelChoiceField(
        label='Ubicación',
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

