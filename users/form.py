from django import forms
from .models import Role, User


class CreateNewUser(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label='Contraseña',
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    confirm_password = forms.CharField(
        label='Confirmar Contraseña',
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
    )
    email = forms.EmailField(
        label='Email',
        max_length=242,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    avatar_file = forms.ImageField(
        label='Foto de avatar (opcional)',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    volunteer_number = forms.CharField(
        label='Numero de Voluntario (opcional)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class LoginUser(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label='Contraseña',
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

class CreateRole(forms.Form):
    name = forms.CharField(
        label='Role',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Role'})
    )

class EditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar_file', 'volunteer_number']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'volunteer_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False