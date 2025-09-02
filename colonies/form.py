from django import forms
from .models import Location, Municipality, Zone, Manager, Colony, Incident, Relief
from users.models import User

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


class MunicipalityForm(forms.ModelForm):
    name = forms.CharField(
        label='Nombre del Municipio',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del municipio'
        })
    )

    zone = forms.ModelChoiceField(
        label='Zona',
        queryset=Zone.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Municipality
        fields = ['name', 'zone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del municipio'}),
            'zone': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nombre del municipio',
            'zone': 'Zona',
        }

class ZoneForm(forms.Form):
    name = forms.CharField(
        label='Nombre de la zona',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la zona'})
    )

class ColonyForm(forms.ModelForm):
    class Meta:
        model = Colony
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la colonia'}),
        }

    location = forms.ModelChoiceField(
        label='Ubicación',
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    manager = forms.ModelChoiceField(
        label='Gestor',
        queryset=Manager.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    users_colony = forms.CharField(
        label='Voluntarios',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción', 'rows': 15})
    )



class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'description', 'start_date', 'end_date', 'is_resolved', 'resolution', 'colony', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describa la incidencia',
                'rows': 4
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_resolved': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_is_resolved',
                'onchange': 'toggleResolutionField()'
            }),
            'resolution': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describa cómo se resolvió la incidencia',
                'rows': 3,
                'id': 'id_resolution'
            }),
            'colony': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cat': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'title': 'Título de la incidencia',
            'description': 'Descripción',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de fin',
            'is_resolved': '¿Está resuelta?',
            'resolution': 'Resolución',
            'colony': 'Colonia',
            'cat': 'Gato'
        }

    def clean(self):
        cleaned_data = super().clean()
        is_resolved = cleaned_data.get('is_resolved')
        resolution = cleaned_data.get('resolution')
        
        # Si está marcado como resuelto, la resolución es obligatoria
        if is_resolved and not resolution:
            raise forms.ValidationError('La resolución es obligatoria cuando la incidencia está marcada como resuelta.')
        
        return cleaned_data

class EditIncident(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'description', 'start_date', 'end_date', 'is_resolved', 'resolution', 'colony']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 4})
        self.fields['start_date'].widget.attrs.update({
            'class': 'form-control',
            'type': 'date'
        })
        self.fields['end_date'].widget.attrs.update({
            'class': 'form-control', 
            'type': 'date'
        })
        self.fields['is_resolved'].widget.attrs.update({
            'class': 'form-check-input',
            'id': 'id_is_resolved',
            'onchange': 'toggleResolutionField()'
        })
        self.fields['resolution'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Describa cómo se resolvió la incidencia',
            'rows': 3,
            'id': 'id_resolution'
        })
        self.fields['colony'].widget.attrs.update({'class': 'form-control'})
        self.fields['cat'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        is_resolved = cleaned_data.get('is_resolved')
        resolution = cleaned_data.get('resolution')
        
        # Si está marcado como resuelto, la resolución es obligatoria
        if is_resolved and not resolution:
            raise forms.ValidationError('La resolución es obligatoria cuando la incidencia está marcada como resuelta.')
        
        return cleaned_data
    
class ReliefForm(forms.Form):
    description = forms.CharField(
        label='Descripción del relevo',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese una descripción',
            'rows': 3
        })
    )

    start_date = forms.DateField(
        label='Fecha de inicio',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Seleccione la fecha de inicio'
        })
    )

    end_date = forms.DateField(
        label='Fecha de finalización',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Seleccione la fecha de finalización'
        })
    )

class EditReliefForm(forms.ModelForm):
    class Meta:
        model = Relief
        fields = ['description', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describa el tipo de alivio proporcionado'
        })

        self.fields['start_date'].widget.attrs.update({
            'class': 'form-control',
            'type': 'date'
        })

        self.fields['end_date'].widget.attrs.update({
            'class': 'form-control',
            'type': 'date'
        })

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('La fecha de inicio no puede ser posterior a la fecha de finalización.')

        return cleaned_data
