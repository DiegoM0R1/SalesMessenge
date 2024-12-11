from django import forms
from .models import Cliente, MensajeGrupo, Mensaje, Cobranza

class LoginForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=100)
    contrasena = forms.CharField(widget=forms.PasswordInput)

from .models import GrupoChat, Usuario

class GrupoChatForm(forms.ModelForm):
    class Meta:
        model = GrupoChat
        fields = ['nombre', 'miembros']
        widgets = {
            'miembros': forms.CheckboxSelectMultiple,
        }


class ClienteForm(forms.ModelForm):
    dni = forms.CharField(
        max_length=8,
        required=False,
        label='DNI',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Cliente
        fields = ['dni', 'nombre', 'email', 'telefono', 'direccion', 'categoria', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(choices=Cliente.CATEGORIA_CLIENTE, attrs={'class': 'form-control'}),
            'estado': forms.Select(choices=Cliente.ESTADO_CLIENTE, attrs={'class': 'form-control'}),
        }

class MensajeGrupoForm(forms.ModelForm):
    class Meta:
        model = MensajeGrupo
        fields = ['contenido', 'tipo', 'archivo']
        widgets = {
            'contenido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe un mensaje...',
                'style': 'padding: 10px; border: 1px solid #ccc; border-radius: 5px;'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'style': 'padding: 10px; border: 1px solid #ccc; border-radius: 5px;'
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'style': 'padding: 10px; border: 1px solid #ccc; border-radius: 5px;'
            }),
        }


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido', 'tipo', 'archivo']
        widgets = {
            'contenido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe un mensaje...',
                'style': 'padding: 10px; border: 1px solid #ccc; border-radius: 5px;'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'style': 'padding: 10px; border: 1px solid #ccc; border-radius: 5px;'
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'style': 'padding: 10px; border: 1px solid #ccc; border-radius: 5px;'
            }),
        }

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['direccion', 'nombre_usuario', 'contrasena', 'foto_perfil']
        widgets = {
            'contrasena': forms.PasswordInput(),
        }

class CobranzaForm(forms.ModelForm):
    class Meta:
        model = Cobranza
        fields = ['monto', 'estado']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

        