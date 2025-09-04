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
    phone = forms.CharField(
        label='Número de teléfono',
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su número de teléfono'})
    )
    carnet_gatos = forms.ImageField(
        label='Carnet de Gatos (opcional)',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
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
    es_capturador = forms.ChoiceField(
        label='¿Es capturador?',
        choices=[('si', 'Sí'), ('no', 'No')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tiene_trampa = forms.ChoiceField(
        label='¿Tiene trampa?',
        choices=[('si', 'Sí'), ('no', 'No')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    es_free = forms.ChoiceField(
        label='¿Es free?',
        choices=[('si', 'Sí'), ('no', 'No')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    association = forms.ModelChoiceField(
        label="Asociación",
        queryset=Association.objects.all(),
        required=False,
        empty_label="-- Selecciona una asociación --",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'association'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'carnet_gatos', 'casa_acogida', 'tiene_relevo', 'es_capturador', 'tiene_trampa', 'es_free', 'association']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'carnet_gatos': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
        
        # Si hay una instancia, configurar los valores iniciales para los campos de elección
        if self.instance and self.instance.pk:
            self.fields['casa_acogida'].initial = 'si' if self.instance.casa_acogida else 'no'
            self.fields['tiene_relevo'].initial = 'si' if self.instance.tiene_relevo else 'no'
            self.fields['es_capturador'].initial = 'si' if self.instance.es_capturador else 'no'
            self.fields['tiene_trampa'].initial = 'si' if self.instance.tiene_trampa else 'no'
            self.fields['es_free'].initial = 'si' if self.instance.es_free else 'no'

        if self.instance.association_id:
                self.fields['association'].initial = self.instance.association

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