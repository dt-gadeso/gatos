from django import forms
from django.core.exceptions import ValidationError
from .models import Cat
from colonies.models import Colony
import datetime

class CreateCat(forms.Form):
    catname = forms.CharField(
        label='Nombre',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cat name'})
    )
    photo_file = forms.ImageField(
        label='Foto',
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    chip = forms.CharField(
        label='Numero de chip',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter chip number'})
    )
    birthday = forms.DateField(
        label='Cumpleaños',
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    sex = forms.ChoiceField(
        label='Sexo',
        choices=[('M', 'Male'), ('F', 'Female')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sterilized = forms.ChoiceField(
        label='Esterilizado',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    dead = forms.ChoiceField(
        label='Muerto',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    colony = forms.ModelChoiceField(
        label='Colonia',
        queryset=Colony.objects.none(),
        required=False,
        empty_label="Selecciona una colonia (opcional)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['colony'].queryset = Colony.objects.filter(user=user)

    def clean_catname(self):
        catname = self.cleaned_data.get('catname')
        if catname:
            catname = catname.strip().title()
            if len(catname) < 2:
                raise ValidationError('Name must be at least 2 characters long.')
        return catname

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
        fields = ['catname', 'photo_file', 'chip', 'birthday', 'sex', 'sterilized', 'dead', 'colony']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)