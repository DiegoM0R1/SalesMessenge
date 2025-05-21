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
        fields = ['contenido', 'tipo', 'archivo'] # 'emisor' y 'grupo' se deben asignar en la vista
        widgets = {
            'contenido': forms.Textarea(attrs={
                'id': 'id_contenido', # Para que coincida con tu JS si lo referencia por ID
                'class': 'input-wrapper-textarea', # Usa una clase específica para el textarea
                'placeholder': 'Escribe un mensaje...',
                'rows': '1'
            }),
            'tipo': forms.Select(attrs={
                'id': 'id_tipo',
                'class': 'd-none' # O tu clase CSS para ocultarlo
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'id': 'id_archivo',
                'class': 'd-none' # O tu clase CSS para ocultarlo
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El default del modelo ya debería establecer 'tipo' a 'texto'.
        # No necesitas 'initial' aquí si el modelo está correcto.

        # Campos no requeridos individualmente, validados en clean()
        self.fields['contenido'].required = False
        self.fields['archivo'].required = False

    def clean(self):
        cleaned_data = super().clean()
        contenido = cleaned_data.get('contenido')
        archivo = cleaned_data.get('archivo')
        # tipo = cleaned_data.get('tipo') # Ya debería ser 'texto' si no se cambió por JS

        if not contenido and not archivo:
            raise forms.ValidationError("Debes escribir un mensaje o adjuntar un archivo.")
        
        # Puedes añadir más validaciones aquí si es necesario
        return cleaned_data


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido', 'tipo', 'archivo']
        widgets = {
            'contenido': forms.Textarea(attrs={ # Cambiado a Textarea
                'id': 'id_contenido', # El JS usa este ID
                'class': 'form-control', # O la clase que uses para tu input de chat
                'placeholder': 'Escribe un mensaje...',
                'rows': '1' # Para que empiece pequeño y el JS lo redimensione
            }),
            'tipo': forms.Select(attrs={
                'id': 'id_tipo', # El JS usa este ID (o name="tipo")
                'class': 'form-control' # O la clase para ocultarlo, ej: 'd-none' o tu clase CSS
                                        # No necesitas el style="" aquí si lo manejas con CSS
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'id': 'id_archivo', # El JS usa este ID (o name="archivo")
                'class': 'form-control-file' # O la clase para ocultarlo
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aunque el modelo ya tiene default='texto', podemos ser explícitos.
        # Si el modelo ya tiene el default, esta línea es redundante pero no daña.
        if not self.initial.get('tipo') and 'tipo' in self.fields:
             self.fields['tipo'].initial = 'texto'

        # Determinar si los campos son requeridos
        # Un mensaje puede ser solo texto, solo archivo, o ambos.
        if 'contenido' in self.fields:
            self.fields['contenido'].required = False
        if 'archivo' in self.fields:
            self.fields['archivo'].required = False


    def clean(self):
        cleaned_data = super().clean()
        contenido = cleaned_data.get('contenido')
        archivo = cleaned_data.get('archivo')
        tipo = cleaned_data.get('tipo') # Ya debería ser 'texto' por defecto

        # Validar que al menos uno de los dos (contenido o archivo) esté presente
        if not contenido and not archivo:
            raise forms.ValidationError(
                "Debes escribir un mensaje o adjuntar un archivo."
            )

        # Si es un tipo de archivo, pero no se proporciona archivo
        if tipo in ['foto', 'video', 'archivo'] and not archivo:
            raise forms.ValidationError(
                f"Para enviar una {tipo.lower()}, debes seleccionar un archivo."
            )
        
        # Si es tipo texto pero se envía un archivo sin contenido (opcional, depende de tu lógica)
        # if tipo == 'texto' and archivo and not contenido:
        #     cleaned_data['tipo'] = 'archivo' # O deducir el tipo del archivo si es posible

        return cleaned_data

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

        