from django import forms
from .models import Role, User, Association


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
    # avatar_file = forms.ImageField(
    #     label='Foto de avatar (opcional)',
    #     required=False,
    #     widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    # )
    carnet_gatos = forms.CharField(
        label='Carnet de Gatos (opcional)',
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

class CreateRole(forms.ModelForm):
    name = forms.CharField(
        label='Role',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Role'})
    )
    class Meta:
        model = Role
        fields = ['name']  

class EditUser(forms.ModelForm):
    casa_acogida = forms.ChoiceField(
        label='Casa de acogida',
        choices=[('si', 'Sí'), ('no', 'No')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tiene_relevo = forms.ChoiceField(
        label='¿Tiene relevo?',
        choices=[('si', 'Sí'), ('no', 'No')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'carnet_gatos', 'casa_acogida', 'tiene_relevo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'carnet_gatos': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
        
        # Si hay una instancia, configurar los valores iniciales para los campos de elección
        if self.instance and self.instance.pk:
            self.fields['casa_acogida'].initial = 'si' if self.instance.casa_acogida else 'no'
            self.fields['tiene_relevo'].initial = 'si' if self.instance.tiene_relevo else 'no'

class AssignedRole(forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        label='Role',
        widget=forms.Select(attrs={'class': 'form-control'})
    ) 
    association = forms.ModelChoiceField(
        queryset=None,
        label='Association',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['role', 'association']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['association'].queryset = Association.objects.all()

class AssociationForm(forms.ModelForm):
    class Meta:
        model = Association
        fields = ['name', 'email', 'phone', 'logo_file', 'location']