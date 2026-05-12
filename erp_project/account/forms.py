
from django import forms
from django.contrib.auth.models import User
from empresa.models import Empresa
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(
        label='Contraseña', widget=forms.PasswordInput
    )


class UserRestrationForm(forms.ModelForm):
    """Registro normal (sin empresa)."""
    password = forms.CharField(
        label='Contraseña', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirmar contraseña', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']


class OwnerRegistrationForm(forms.ModelForm):
    """
    Registro del dueño: crea User + Empresa + UserProfile(owner).
    """
    password = forms.CharField(
        label='Contraseña', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirmar contraseña', widget=forms.PasswordInput
    )

    razon_social = forms.CharField(
        max_length=200, help_text="Nombre del negocio"
    )
    rut = forms.CharField(
        max_length=20, required=False, help_text="RUT de la empresa"
    )
    direccion = forms.CharField(
        max_length=255, required=False, help_text="Dirección"
    )
    telefono = forms.CharField(
        max_length=20, required=False, help_text="Teléfono de la empresa"
    )
    email_empresa = forms.EmailField(
        required=False, help_text="Correo de contacto de la empresa"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este email.")
        return email

    def save(self, commit=True):
        """
        Crea:
          - Empresa
          - User
          - UserProfile(rol=owner, es_dueno=True)
        """
        # 1. Crear empresa
        empresa = Empresa.objects.create(
            razon_social=self.cleaned_data['razon_social'],
            rut=self.cleaned_data.get('rut', ''),
            direccion=self.cleaned_data.get('direccion', ''),
            telefono=self.cleaned_data.get('telefono', ''),
            email=self.cleaned_data.get('email_empresa', ''),
        )
        # 2. Crear user
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                empresa=empresa,
                rol='owner',
                es_dueno=True,
                activo=True,
            )
        return user


class SubcuentaForm(forms.ModelForm):
    """
    Formulario para crear subcuentas (usuarios dentro de la misma empresa).
    Solo el dueño/admin puede crearlos; no se pide email.
    """
    password = forms.CharField(
        label='Contraseña temporal', widget=forms.PasswordInput
    )
    rol = forms.ChoiceField(
        choices=[
            ('administrador', 'Administrador'),
            ('supervisor', 'Supervisor'),
            ('empleado', 'Empleado'),
            ('contador', 'Contador'),
        ],
        initial='empleado'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def save(self, empresa, rol='empleado', commit=True):
        user = User(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email='',  # Vacío; solo para el dueño en el caso general
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                empresa=empresa,
                rol=rol,
                activo=True,
            )
        return user