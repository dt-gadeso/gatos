from django import forms
from colonies.models import Municipality, Location
from users.models import User, Association
from cats.models import Cat
from .models import VetCenter, Visit
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and hasattr(user, 'association') and user.association:
            from colonies.models import Location
            association_locations = Location.objects.filter(
                zone__municipality__in=user.association.municipalities.all()
            ) if hasattr(user.association, 'municipalities') else Location.objects.all()
            
            self.fields['location'].queryset = association_locations
            
            if association_locations.count() == 0:
                self.fields['location'].widget.attrs['disabled'] = True
                self.fields['location'].help_text = "No hay ubicaciones disponibles para tu asociación."
        else:
            from colonies.models import Location
            self.fields['location'].queryset = Location.objects.all()

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['colony', 'colony_user','cat', 'vet_center', 'price', 'report_file', 'bill_file', 'user', 'follow_up', 'start_date', 'end_date', 'cat_survived', 'returned_to_colony', 'housing_type', 'housing_address']
        widgets = {
            'cat_survived': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_cat_survived',
            }, choices=[('True', 'Sí'), ('False', 'No')]),
            'returned_to_colony': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_returned_to_colony',
            }, choices=[('True', 'Sí'), ('False', 'No')]),
            'housing_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_housing_type',
            }),
            'housing_address': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'id_housing_address',
                'rows': 3,
            }),
            'colony': forms.Select(attrs={'class': 'form-control'}),
            'colony_user': forms.Select(attrs={'class': 'form-control'}),
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
            }),
            'cat_survived': forms.Select(attrs={'class': 'form-select'}, choices=[(True, 'Sí'), (False, 'No')]),
            'returned_to_colony': forms.Select(attrs={'class': 'form-select'}, choices=[(True, 'Sí'), (False, 'No')]),
            'housing_type': forms.Select(attrs={'class': 'form-select'}),
            'housing_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
        labels = {
            'colony': 'Colonia',
            'colony_user': 'Gestor de colonia',
            'cat': 'Gato',
            'vet_center': 'Centro veterinario',
            'price': 'Precio',
            'report_file': 'Archivo del informe (opcional)',
            'bill_file': 'Archivo de la factura (opcional)',
            'user': 'Usuario',
            'follow_up': 'Seguimiento',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de fin',
            'cat_survived': '¿El gato sobrevivió?'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and hasattr(user, 'association') and user.association:
            vet_centers = VetCenter.objects.all()
            
            self.fields['vet_center'].queryset = vet_centers
            
            self.fields['user'].initial = user
            
            if vet_centers.count() == 0:
                self.fields['vet_center'].queryset = VetCenter.objects.none()
                self.fields['vet_center'].widget.attrs['disabled'] = True
                self.fields['vet_center'].help_text = "No hay centros veterinarios disponibles."
            
            if hasattr(user, 'association') and user.association:
                pass
        else:
            self.fields['vet_center'].queryset = VetCenter.objects.all()

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

    def save(self, commit=True):
        visit = super().save(commit=False)
        
        if not visit.cat_survived:
            cat = visit.cat
            cat.dead = True
            if commit:
                cat.save()
        
        if commit:
            visit.save()

        return visit
       