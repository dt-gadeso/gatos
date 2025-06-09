from django import forms
from .models import MapPopup, Location, Municipality, Zone

class PopupForm(forms.ModelForm):
    """Formulario para crear popups dinámicos"""
    
    # Campo personalizado para buscar ubicaciones
    location_search = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar dirección...',
            'id': 'location-search'
        }),
        label="Buscar Ubicación"
    )
    
    class Meta:
        model = MapPopup
        fields = ['title', 'description', 'location', 'popup_html', 'icon_color']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del popup'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del lugar'
            }),
            'location': forms.Select(attrs={
                'class': 'form-control'
            }),
            'popup_html': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'HTML personalizado (opcional)'
            }),
            'icon_color': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar ubicaciones por municipio
        self.fields['location'].queryset = Location.objects.select_related(
            'municipality', 'municipality__zone'
        ).order_by('municipality__name', 'address')

class QuickLocationForm(forms.ModelForm):
    """Formulario rápido para crear ubicaciones desde coordenadas"""
    latitude = forms.DecimalField(
        max_digits=10,
        decimal_places=8,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': 'any',
            'placeholder': '41.383'
        })
    )
    longitude = forms.DecimalField(
        max_digits=11,
        decimal_places=8,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': 'any',
            'placeholder': '2.178'
        })
    )
    
    class Meta:
        model = Location
        fields = ['address', 'municipality', 'latitude', 'longitude']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa'
            }),
            'municipality': forms.Select(attrs={
                'class': 'form-control'
            })
        }