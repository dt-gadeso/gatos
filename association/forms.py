from django import forms
from .models import Association

class AssociationForm(forms.ModelForm):
    class Meta:
        model = Association
        fields = ['name', 'email', 'phone', 'logo_file', 'location']