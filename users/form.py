from django import forms
from .models import Role, User, Association, TrapType


class CreateNewUser(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'new-password'
        })
    )
    confirm_password = forms.CharField(
        label='Confirmar Contraseña',
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password'
        })
    )
    email = forms.EmailField(
        label='Email',
        max_length=242,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autocomplete': 'email'
        })
    )
    phone = forms.CharField(
        label='Número de teléfono',
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su número de teléfono',
            'autocomplete': 'tel'
        })
    )
    carnet_gatos = forms.ImageField(
        label='Carnet de Gatos (opcional)',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    es_capturador = forms.ChoiceField(
        label='¿Es capturador?',
        choices=[('no', 'No'), ('si', 'Sí')],
        initial='no',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_es_capturador',
            'autocomplete': 'off'  # Desactivamos el autocompletado para campos de selección
        })
    )
    trap_type = forms.ModelChoiceField(
        label='Tipo de trampa',
        queryset=TrapType.objects.all(),
        required=False,
        empty_label='Selecciona el tipo de trampa',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_trap_type',
            'autocomplete': 'off'  # Desactivamos el autocompletado para campos de selección
        })
    )

class LoginUser(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password'
        })
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
    trap_type = forms.ModelChoiceField(
        label='Tipo de trampa',
        queryset=TrapType.objects.all(),
        required=False,
        empty_label='No tiene trampa',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    es_free = forms.ChoiceField(
        label='¿Tienes associacion?',
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
        fields = ['username', 'email', 'phone', 'carnet_gatos', 'casa_acogida', 'tiene_relevo', 'es_capturador', 'trap_type', 'es_free', 'association']
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
        
        if self.instance and self.instance.pk:
            self.fields['casa_acogida'].initial = 'si' if self.instance.casa_acogida else 'no'
            self.fields['tiene_relevo'].initial = 'si' if self.instance.tiene_relevo else 'no'
            self.fields['es_capturador'].initial = 'si' if self.instance.es_capturador else 'no'
            self.fields['es_free'].initial = 'si' if self.instance.es_free else 'no'
            if self.instance.es_capturador:
                self.fields['trap_type'].widget.attrs['disabled'] = False
            else:
                self.fields['trap_type'].widget.attrs['disabled'] = True

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