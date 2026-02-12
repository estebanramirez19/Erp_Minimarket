from django import forms
from django.forms import inlineformset_factory

from .models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'