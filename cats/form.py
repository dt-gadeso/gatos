from django import forms
from django.core.exceptions import ValidationError
from .models import Cat
from colonies.models import Colony
import datetime

class CreateCat(forms.Form):
    catname = forms.CharField(
        label='Nombre del gato',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del gato'})
    )
    photo_file = forms.ImageField(
        label='Foto del gato',
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    chip = forms.CharField(
        label='Número de chip',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de chip'})
    )
    birthday = forms.DateField(
        label='Fecha de nacimiento',
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    sex = forms.ChoiceField(
        label='Sexo',
        choices=[('M', 'Macho'), ('F', 'Hembra')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sterilized = forms.ChoiceField(
        label='Esterilizado',
        choices=[('true', 'Sí'), ('false', 'No')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        label='Estado del gato',
        choices=[('V', 'Vivo'), ('E', 'Enfermo'), ('M', 'Muerto')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    colony = forms.ModelChoiceField(
        label='Colonia',
        queryset=Colony.objects.all(),
        empty_label="Selecciona una colonia",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['colony'].queryset = Colony.objects.all()

    def clean_catname(self):
        catname = self.cleaned_data.get('catname')
        if catname:
            catname = catname.strip().title()
            if len(catname) < 2:
                raise ValidationError('Name must be at least 2 characters long.')
        return catname

    def clean_chip(self):
        chip = self.cleaned_data.get('chip')
        if chip:
            if Cat.objects.filter(chip=chip).exists():
                raise ValidationError('Ya existe un gato con este número de chip.')
        return chip

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday:
            today = datetime.date.today()
            if birthday > today:
                raise ValidationError('Birthday cannot be in the future.')
            if (today - birthday).days > (25 * 365):
                raise ValidationError('Birthday seems too old.')
        return birthday

class EditCat(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ['catname', 'photo_file', 'chip', 'birthday', 'sex', 'sterilized', 'status', 'colony']
        widgets = {
            'catname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del gato'}),
            'photo_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'chip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de chip'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sex': forms.Select(attrs={'class': 'form-control form-select'}),
            'sterilized': forms.Select(attrs={'class': 'form-control form-select'}),
            'status': forms.Select(attrs={'class': 'form-control form-select'}),
            'colony': forms.Select(attrs={'class': 'form-control form-select'}),
        }
        labels = {
            'catname': 'Nombre del gato',
            'photo_file': 'Foto del gato',
            'chip': 'Número de chip',
            'birthday': 'Fecha de nacimiento',
            'sex': 'Sexo',
            'sterilized': 'Esterilizado',
            'status': 'Estado del gato',
            'colony': 'Colonia',
        }
    
    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['colony'].queryset = Colony.objects.all()

class SearchCatForm(forms.Form):
    catname = forms.CharField(
        label='Nombre del gato',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nombre del gato'
        })
    )
    colony = forms.ModelChoiceField(
        label='Colonia',
        queryset=Colony.objects.all(),
        required=False,
        empty_label="Seleccionar colonia",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sex = forms.ChoiceField(
        label='Sexo',
        choices=[('', 'Seleccionar sexo'), ('M', 'Macho'), ('F', 'Hembra')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sterilized = forms.ChoiceField(
        label='¿Esterilizado?',
        choices=[('', 'Seleccionar estado'), ('true', 'Sí'), ('false', 'No')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        label='Estado',
        choices=[('', 'Seleccionar estado'), ('V', 'Vivo'), ('E', 'Enfermo'), ('M', 'Fallecido')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['colony'].queryset = Colony.objects.all()