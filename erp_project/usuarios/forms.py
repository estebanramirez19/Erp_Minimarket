from django import forms
from .models import PerfilUsuario

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['user','rol', 'nombre', 'apellido', 'email', 'telefono', 'foto_perfil', 'activo', 'contraseña'] 
        widgets = {
            "user": forms.Select(),
            "rol": forms.Select(),
            "nombre": forms.TextInput(attrs={'placeholder': 'Ingrese su nombre'}),
            "apellido": forms.TextInput(attrs={'placeholder': 'Ingrese su apellido'}),
            "email": forms.EmailInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
            "telefono": forms.TextInput(attrs={'placeholder': 'Ingrese su número de teléfono'}),
            "foto_perfil": forms.ClearableFileInput(),
            "activo": forms.CheckboxInput(),
            "contraseña": forms.PasswordInput(attrs={'placeholder': 'Ingrese una contraseña'}),
        }
