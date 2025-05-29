from django import forms
from django.core.exceptions import ValidationError
from .models import Cat
from colonies.models import Colony
import datetime

class CreateCat(forms.Form):
    catname = forms.CharField(
        label='Name',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cat name'})
    )
    photo_file = forms.ImageField(
        label='Photo',
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    chip = forms.CharField(
        label='Chip Number',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter chip number'})
    )
    birthday = forms.DateField(
        label='Birthday',
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    sex = forms.ChoiceField(
        label='Sex',
        choices=[('M', 'Male'), ('F', 'Female')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sterilized = forms.ChoiceField(
        label='Sterilized',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    dead = forms.ChoiceField(
        label='Dead',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    colony = forms.ModelChoiceField(
        label='Colony',
        queryset=Colony.objects.none(),
        required=False,
        empty_label="Select a colony (optional)",
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

class EditCat(forms.Form):
    catname = forms.CharField(
        label='Name',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cat name'})
    )
    photo_file = forms.ImageField(
        label='Photo',
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    chip = forms.CharField(
        label='Chip Number',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter chip number'})
    )
    birthday = forms.DateField(
        label='Birthday',
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    sex = forms.ChoiceField(
        label='Sex',
        choices=[('M', 'Male'), ('F', 'Female')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sterilized = forms.ChoiceField(
        label='Sterilized',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    dead = forms.ChoiceField(
        label='Dead',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    colony = forms.ModelChoiceField(
        label='Colony',
        queryset=Colony.objects.none(),
        required=False,
        empty_label="Select a colony (optional)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        cat_instance = kwargs.pop('cat_instance', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['colony'].queryset = Colony.objects.filter(user=user)
        
        self.cat_instance = cat_instance

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