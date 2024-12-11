from django.db import models

class Usuario(models.Model):
    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('trabajador', 'Trabajador de área'),
    ]
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=250)
    fecha_nacimiento = models.DateField()
    nombre_usuario = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO, default='trabajador')
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Mensaje(models.Model):
    emisor = models.ForeignKey(Usuario, related_name='mensajes_enviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey(Usuario, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    tipo = models.CharField(max_length=10, choices=[('texto', 'Texto'), ('foto', 'Foto'), ('video', 'Video'), ('archivo', 'Archivo')])
    archivo = models.FileField(upload_to='archivos/', null=True, blank=True)

class GrupoChat(models.Model):
    nombre = models.CharField(max_length=100)
    miembros = models.ManyToManyField(Usuario)

def __str__(self):
        return self.nombre

class MensajeGrupo(models.Model):
    grupo = models.ForeignKey(GrupoChat, related_name='mensajes', on_delete=models.CASCADE)
    emisor = models.ForeignKey(Usuario, related_name='mensajes_enviados_grupo', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    tipo = models.CharField(max_length=10, choices=[('texto', 'Texto'), ('foto', 'Foto'), ('video', 'Video'), ('archivo', 'Archivo')])
    archivo = models.FileField(upload_to='archivos/', null=True, blank=True)


class Cliente(models.Model):
    CATEGORIA_CLIENTE = [
        ('A', 'Cliente de alto valor'),
        ('B', 'Cliente de valor medio'),
        ('C', 'Cliente de bajo valor'),
        ('VIP', 'Cliente muy importante'),
        ('Nuevo', 'Cliente nuevo'),
        ('Frecuente', 'Cliente frecuente'),
        ('Ocasional', 'Cliente ocasional'),
    ]
    ESTADO_CLIENTE = [
        ('activo', 'Activo'),
        ('prospecto', 'Prospecto'),
        ('inactivo', 'Inactivo'),
    ]
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=250)
    dni = models.CharField(max_length=8, unique=True)  # Agregar campo DNI
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CLIENTE, default='Nuevo')
    estado = models.CharField(max_length=10, choices=ESTADO_CLIENTE, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # campo nuevo

    def __str__(self):
        return self.nombre
    
    
class Oportunidad(models.Model):
    ESTADO_OPORTUNIDAD = [
        ('prospecto', 'Prospecto'),
        ('negociacion', 'En Negociación'),
        ('cerrado', 'Cerrado'),
        ('seguimiento', 'Seguimiento'),
    ]
    cliente = models.ForeignKey(Cliente, related_name='oportunidades', on_delete=models.CASCADE)
    descripcion = models.TextField(default='Sin descripción')  # Definir un valor predeterminado
    estado = models.CharField(max_length=50, choices=ESTADO_OPORTUNIDAD, default='prospecto')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Cotizacion(models.Model):
    oportunidad = models.ForeignKey(Oportunidad, related_name='cotizaciones', on_delete=models.CASCADE)
    descripcion = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=[('enviada', 'Enviada'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')])

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='facturas', on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=[('pendiente', 'Pendiente'), ('pagada', 'Pagada')], default='pendiente')

class Ingreso(models.Model):
    factura = models.ForeignKey(Factura, related_name='ingresos', on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    origen = models.CharField(max_length=50, choices=[
        ('venta', 'Venta'),
        ('cobranza', 'Cobranza'),
        ('otro', 'Otro')
    ])

class Cobranza(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='cobranzas', on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, related_name='cobranzas', on_delete=models.CASCADE)
    fecha_cobranza = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=[
        ('parcial', 'Parcial'),
        ('total', 'Total')
    ], default='parcial')

    def __str__(self):
        return f"Cobranza de {self.monto} para la factura {self.factura.id}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total_pagado = sum(cobranza.monto for cobranza in self.factura.cobranzas.all())
        if total_pagado >= self.factura.total:
            self.factura.estado = 'pagada'
        else:
            self.factura.estado = 'pendiente'
        self.factura.save()
       
class Consulta(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='consultas', on_delete=models.CASCADE)
    descripcion = models.TextField()
    estado = models.CharField(max_length=50, choices=[('pendiente', 'Pendiente'), ('resuelto', 'Resuelto')], default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)