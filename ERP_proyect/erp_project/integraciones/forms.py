from django import forms
from .models import LecturaCodigo, ImagenProducto

class LecturaCodigoForm(forms.ModelForm):
    class Meta:
        model = LecturaCodigo
        fields = ["producto", "codigo"]

    def clean_codigo(self):
        codigo = self.cleaned_data.get("codigo")
        # ejemplo: validación simple
        if not codigo:
            raise forms.ValidationError("El código es obligatorio.")
        return codigo

class ImagenProductoForm(forms.ModelForm):
    class Meta:
        model = ImagenProducto
        fields = ["producto", "imagen", "descripcion"]

    def clean_imagen(self):
        imagen = self.cleaned_data.get("imagen")
        # ejemplo: limitar tamaño de imagen (opcional)
        if imagen and imagen.size > 5 * 1024 * 1024:
            raise forms.ValidationError("La imagen no puede superar 5 MB.")
        return imagen