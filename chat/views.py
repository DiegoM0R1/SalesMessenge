# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Mensaje, Cliente, Oportunidad, Cotizacion, Factura, Ingreso, Cobranza, Consulta, GrupoChat, MensajeGrupo
from .forms import LoginForm, GrupoChatForm, MensajeGrupoForm, EditarUsuarioForm, CobranzaForm, MensajeForm
from django.utils import timezone  # Importar timezone
from django.db.models import Q  # Importar Q
import os
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_usuario']
            contrasena = form.cleaned_data['contrasena']
            try:
                usuario = Usuario.objects.get(nombre_usuario=nombre_usuario, contrasena=contrasena)
                request.session['usuario_id'] = usuario.id
                return redirect('lista_usuarios')
            except Usuario.DoesNotExist:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'chat/login.html', {'form': form})
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cliente

@csrf_exempt
def buscar_cliente_por_dni(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        if not dni:
            return JsonResponse({'error': 'DNI es requerido'}, status=400)
        
        token = 'de3e5dc9486d29e79d5d497fa4082ba9f18472e6a1ec9686de1e35e6c0be81d7'
        
        # Primer intento: GET con parámetros en URL
        try:
            url = f'https://apiperu.dev/api/dni/{dni}?api_token={token}'
            response = requests.get(url)
            print(f"GET Status Code: {response.status_code}")  # Debug
            print(f"GET Response: {response.text}")  # Debug
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    # Devolver los datos encontrados sin guardar en la base de datos
                    return JsonResponse({
                        'nombre': data['data'].get('nombre_completo', ''),
                        'email': '',
                        'telefono': '',
                        'direccion': '',
                        'dni': dni,
                        'categoria': 'Nuevo',
                        'estado': 'activo',
                    })
            
            # Si el GET falla, intentamos POST
            url = 'https://apiperu.dev/api/dni'
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            payload = {'dni': dni}
            
            response = requests.post(url, headers=headers, json=payload)
            print(f"POST Status Code: {response.status_code}")  # Debug
            print(f"POST Response: {response.text}")  # Debug
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    # Devolver los datos encontrados sin guardar en la base de datos
                    return JsonResponse({
                        'nombre': data['data'].get('nombre_completo', ''),
                        'email': '',
                        'telefono': '',
                        'direccion': '',
                        'dni': dni,
                        'categoria': 'Nuevo',
                        'estado': 'activo',
                    })
                else:
                    # Devolver el DNI proporcionado si no se encontraron datos
                    return JsonResponse({
                        'nombre': '',
                        'email': '',
                        'telefono': '',
                        'direccion': '',
                        'dni': dni,
                        'categoria': 'Nuevo',
                        'estado': 'activo',
                    })
            else:
                return JsonResponse({
                    'error': 'Error al consultar la API',
                    'detail': response.text
                }, status=response.status_code)
                
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug
            return JsonResponse({'error': f'Error de conexión: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def lista_usuarios(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_actual_id = request.session.get('usuario_id')
    usuario_actual = Usuario.objects.get(id=usuario_actual_id)
    usuarios = Usuario.objects.exclude(id=usuario_actual_id)
    return render(request, 'chat/lista_usuarios.html', {'usuarios': usuarios, 'usuario_actual': usuario_actual})

def editar_perfil(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session.get('usuario_id')
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('editar_perfil')
    else:
        form = EditarUsuarioForm(instance=usuario)
    return render(request, 'chat/editar_perfil.html', {'form': form})


def chat(request, usuario_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_actual_id = request.session.get('usuario_id')
    usuario_actual = Usuario.objects.get(id=usuario_actual_id)
    usuario = Usuario.objects.get(id=usuario_id)
    mensajes = Mensaje.objects.filter(
        (Q(emisor=usuario_actual) & Q(receptor=usuario)) |
        (Q(emisor=usuario) & Q(receptor=usuario_actual))
    ).order_by('fecha_hora')
    if request.method == 'POST':
        form = MensajeForm(request.POST, request.FILES)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = usuario_actual
            mensaje.receptor = usuario
            mensaje.save()
            return redirect('chat', usuario_id=usuario.id)
    else:
        form = MensajeForm()
    return render(request, 'chat/chat.html', {'usuario': usuario, 'mensajes': mensajes, 'form': form})

#crear grupo de chat
def crear_grupo_chat(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_actual_id = request.session.get('usuario_id')
    usuario_actual = Usuario.objects.get(id=usuario_actual_id)
    if usuario_actual.tipo_usuario != 'admin':
        return redirect('lista_usuarios')
    if request.method == 'POST':
        form = GrupoChatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_grupos_chat')
    else:
        form = GrupoChatForm()
    return render(request, 'chat/crear_grupo_chat.html', {'form': form})

def lista_grupos_chat(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    grupos = GrupoChat.objects.all()
    return render(request, 'chat/lista_grupos_chat.html', {'grupos': grupos})

def editar_grupo_chat(request, grupo_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    grupo = get_object_or_404(GrupoChat, id=grupo_id)
    if request.method == 'POST':
        form = GrupoChatForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            return redirect('lista_grupos_chat')
    else:
        form = GrupoChatForm(instance=grupo)
    return render(request, 'chat/editar_grupo_chat.html', {'form': form})

def eliminar_grupo_chat(request, grupo_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    grupo = get_object_or_404(GrupoChat, id=grupo_id)
    grupo.delete()
    return redirect('lista_grupos_chat')

def chat_grupo(request, grupo_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    grupo = get_object_or_404(GrupoChat, id=grupo_id)
    mensajes = MensajeGrupo.objects.filter(grupo=grupo).order_by('fecha_hora')
    if request.method == 'POST':
        form = MensajeGrupoForm(request.POST, request.FILES)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = Usuario.objects.get(id=request.session['usuario_id'])
            mensaje.grupo = grupo
            mensaje.save()
            return redirect('chat_grupo', grupo_id=grupo.id)
    else:
        form = MensajeGrupoForm()
    return render(request, 'chat/chat_grupo.html', {'grupo': grupo, 'mensajes': mensajes, 'form': form})

def enviar_mensaje(request, usuario_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        emisor_id = request.session.get('usuario_id')
        if not emisor_id:
            return redirect('login')
        emisor = Usuario.objects.get(id=emisor_id)
        receptor = Usuario.objects.get(id=usuario_id)
        contenido = request.POST['contenido']
        tipo = request.POST['tipo']
        archivo = request.FILES.get('archivo')
        Mensaje.objects.create(emisor=emisor, receptor=receptor, contenido=contenido, tipo=tipo, archivo=archivo)
        return redirect('chat', usuario_id=usuario_id)
    return redirect('lista_usuarios')

LoginForm

def registrar_usuario(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_actual_id = request.session.get('usuario_id')
    usuario_actual = Usuario.objects.get(id=usuario_actual_id)
    if usuario_actual.tipo_usuario != 'admin':
        return redirect('lista_usuarios')
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        codigo = request.POST['codigo']
        direccion = request.POST['direccion']
        fecha_nacimiento = request.POST['fecha_nacimiento']
        nombre_usuario = request.POST['nombre_usuario']
        contrasena = request.POST['contrasena']
        tipo_usuario = request.POST['tipo_usuario']
        Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            codigo=codigo,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            nombre_usuario=nombre_usuario,
            contrasena=contrasena,
            tipo_usuario=tipo_usuario
        )
        return redirect('lista_usuarios')
    return render(request, 'chat/registrar_usuario.html')

def editar_usuario(request, usuario_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_actual_id = request.session.get('usuario_id')
    usuario_actual = Usuario.objects.get(id=usuario_actual_id)
    if usuario_actual.tipo_usuario != 'admin':
        return redirect('lista_usuarios')
    usuario = Usuario.objects.get(id=usuario_id)
    if request.method == 'POST':
        usuario.nombre = request.POST['nombre']
        usuario.apellido = request.POST['apellido']
        usuario.codigo = request.POST['codigo']
        usuario.direccion = request.POST['direccion']
        usuario.fecha_nacimiento = request.POST['fecha_nacimiento']
        usuario.nombre_usuario = request.POST['nombre_usuario']
        usuario.contrasena = request.POST['contrasena']
        usuario.tipo_usuario = request.POST['tipo_usuario']
        usuario.save()
        return redirect('lista_usuarios')
    return render(request, 'chat/editar_usuario.html', {'usuario': usuario})

def eliminar_usuario(request, usuario_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_actual_id = request.session.get('usuario_id')
    usuario_actual = Usuario.objects.get(id=usuario_actual_id)
    if usuario_actual.tipo_usuario != 'admin':
        return redirect('lista_usuarios')
    usuario = Usuario.objects.get(id=usuario_id)
    usuario.delete()
    return redirect('lista_usuarios')


def backup_database(request):
    db_path = settings.DATABASES['default']['NAME']
    backup_path = os.path.join(settings.BASE_DIR, 'db_backup.sqlite3')
    with open(db_path, 'rb') as db_file, open(backup_path, 'wb') as backup_file:
        backup_file.write(db_file.read())
    response = HttpResponse(open(backup_path, 'rb').read(), content_type='application/x-sqlite3')
    response['Content-Disposition'] = f'attachment; filename="db_backup.sqlite3"'
    return response

import plotly.express as px
import plotly.io as pio
from django.db.models import Count, Sum, F
from datetime import datetime, timedelta

#dashboard de la aplicación
def dashboard(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    total_clientes = Cliente.objects.count() 
    clientes_activos = Cliente.objects.filter(estado='activo').count()
    clientes_inactivos = Cliente.objects.filter(estado='inactivo').count()
    clientes_prospectos = Cliente.objects.filter(estado='prospecto').count()
    
    actividad_reciente = Consulta.objects.order_by('-fecha_creacion')[:10]
    
    # Datos para el gráfico de pastel
    labels = ['Activos', 'Inactivos', 'Prospectos']
    sizes = [clientes_activos, clientes_inactivos, clientes_prospectos]
    
    # Crear gráfico de pastel con Plotly
    fig = px.pie(values=sizes, names=labels, title='Segmentación de Clientes')
    chart_html = pio.to_html(fig, full_html=False)
    
    # Datos para el pipeline de ventas
    pipeline_data = Oportunidad.objects.values('estado').annotate(total=Count('estado'))
    pipeline_labels = [item['estado'] for item in pipeline_data]
    pipeline_values = [item['total'] for item in pipeline_data]
    
    # Crear gráfico de barras con Plotly
    fig_bar = px.bar(x=pipeline_labels, y=pipeline_values, title='Pipeline de Ventas')
    chart_bar_html = pio.to_html(fig_bar, full_html=False)
    
    # Crear gráfico de embudo con Plotly
    fig_funnel = px.funnel(x=pipeline_labels, y=pipeline_values, title='Pipeline de Ventas (Embudo)')
    chart_funnel_html = pio.to_html(fig_funnel, full_html=False)
    
     # Calcular ingresos totales y ventas totales
    ingresos_totales = Ingreso.objects.aggregate(total=Sum('monto'))['total'] or 0
    ventas_totales = Factura.objects.aggregate(total=Sum('total'))['total'] or 0
    
    # Calcular nuevos clientes del mes
    inicio_mes = datetime.now().replace(day=1)
    nuevos_clientes = Cliente.objects.filter(fecha_creacion__gte=inicio_mes).count()
    
    # Calcular ventas del mes
    ventas_mes = Factura.objects.filter(fecha_emision__gte=inicio_mes).aggregate(total=Sum('total'))['total'] or 0
    
    # Calcular ventas del mes anterior
    inicio_mes_anterior = (inicio_mes - timedelta(days=1)).replace(day=1)
    fin_mes_anterior = inicio_mes - timedelta(days=1)
    ventas_mes_anterior = Factura.objects.filter(fecha_emision__gte=inicio_mes_anterior, fecha_emision__lte=fin_mes_anterior).aggregate(total=Sum('total'))['total'] or 0
    
    # Crear gráfico de barras comparando ventas del mes anterior con el actual
    fig_ventas = px.bar(
        x=['Mes Anterior', 'Mes Actual'],
        y=[ventas_mes_anterior, ventas_mes],
        title='Comparación de Ventas: Mes Anterior vs Mes Actual'
    )
    chart_ventas_html = pio.to_html(fig_ventas, full_html=False)
    

    context = {
        'total_clientes': total_clientes,
        'clientes_activos': clientes_activos,
        'clientes_inactivos': clientes_inactivos,
        'clientes_prospectos': clientes_prospectos,
        'actividad_reciente': actividad_reciente,
        'chart_html': chart_html,
        'chart_bar_html': chart_bar_html,
        'chart_funnel_html': chart_funnel_html,
        'ingresos_totales': ingresos_totales,
        'ventas_totales': ventas_totales,
        'nuevos_clientes': nuevos_clientes,
        'ventas_mes': ventas_mes,
        'chart_ventas_html': chart_ventas_html,
   
    }
    
    return render(request, 'chat/dashboard.html', context)

def logout(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    return redirect('login')




# Lista de Clientes
def lista_clientes(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    clientes = Cliente.objects.all()
    return render(request, 'chat/lista_clientes.html', {'clientes': clientes})

# Detalle del Cliente
def detalle_cliente(request, cliente_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'chat/detalle_cliente.html', {'cliente': cliente})

# Registrar Cliente
from .forms import ClienteForm

def registrar_cliente(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'chat/registrar_cliente.html', {'form': form})

# Editar Cliente
def editar_cliente(request, cliente_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'chat/editar_cliente.html', {'form': form})

# Eliminar Cliente
def eliminar_cliente(request, cliente_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('lista_clientes')

# visualizar los clientes de acuerdo a su estado
def lista_clientes_segmentados(request, estado):
    if 'usuario_id' not in request.session:
        return redirect('login')
    clientes = Cliente.objects.filter(estado=estado)
    return render(request, 'chat/lista_clientes_segmentados.html', {'clientes': clientes, 'estado': estado})

import requests
from django.http import JsonResponse

def buscar_cliente_api(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    nombre_completo = request.GET.get('nombre_completo')
    if not nombre_completo:
        return JsonResponse({'error': 'Nombre completo es requerido'}, status=400)

    # URL de la API externa (por ejemplo, API de RENIEC)
    api_url = 'https://api.reniec.gob.pe/v1/clientes'
    params = {'nombre_completo': nombre_completo}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        return JsonResponse(data)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
#api
from rest_framework import generics
from .models import Cliente
from .serializers import ClienteSerializer

class ClienteListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
#buscar
def buscar(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    query = request.GET.get('q')
    module = request.GET.get('module')
    resultados = []

    if module == 'usuarios':
        resultados = Usuario.objects.filter(nombre_usuario__icontains=query)
    elif module == 'clientes':
        resultados = Cliente.objects.filter(nombre__icontains=query)
    # Añadir más módulos según sea necesario

    return render(request, 'chat/resultados_busqueda.html', {'resultados': resultados, 'module': module})

# Lista de Oportunidades
def lista_oportunidades(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    oportunidades = Oportunidad.objects.all()
    return render(request, 'chat/lista_oportunidades.html', {'oportunidades': oportunidades})

# Detalle de Oportunidad
def detalle_oportunidad(request, oportunidad_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    oportunidad = get_object_or_404(Oportunidad, id=oportunidad_id)
    return render(request, 'chat/detalle_oportunidad.html', {'oportunidad': oportunidad})

# Registrar Oportunidad
def registrar_oportunidad(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        descripcion = request.POST.get('descripcion')
        valor = request.POST.get('valor')
        estado = request.POST.get('estado')
        
        if not cliente_id or not descripcion or not valor or not estado:
            return render(request, 'chat/registrar_oportunidad.html', {
                'clientes': Cliente.objects.all(),
                'error': 'Todos los campos son obligatorios.'
            })
        
        cliente = get_object_or_404(Cliente, id=cliente_id)
        Oportunidad.objects.create(cliente=cliente, descripcion=descripcion, valor=valor, estado=estado)
        return redirect('lista_oportunidades')
    
    clientes = Cliente.objects.all()
    return render(request, 'chat/registrar_oportunidad.html', {'clientes': clientes})
# Editar Oportunidad
def editar_oportunidad(request, oportunidad_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    oportunidad = get_object_or_404(Oportunidad, id=oportunidad_id)
    if request.method == 'POST':
        oportunidad.descripcion = request.POST.get('descripcion', oportunidad.descripcion)
        oportunidad.valor = request.POST.get('valor', oportunidad.valor)
        oportunidad.estado = request.POST.get('estado', oportunidad.estado)
        oportunidad.save()
        return redirect('detalle_oportunidad', oportunidad_id=oportunidad.id)
    return render(request, 'chat/editar_oportunidad.html', {'oportunidad': oportunidad})
# Eliminar Oportunidad
def eliminar_oportunidad(request, oportunidad_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    oportunidad = get_object_or_404(Oportunidad, id=oportunidad_id)
    oportunidad.delete()
    return redirect('lista_oportunidades')

# Lista de Cotizaciones
def lista_cotizaciones(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    cotizaciones = Cotizacion.objects.all()
    return render(request, 'chat/lista_cotizaciones.html', {'cotizaciones': cotizaciones})

# Detalle de Cotización
def detalle_cotizacion(request, cotizacion_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    return render(request, 'chat/detalle_cotizacion.html', {'cotizacion': cotizacion})



# Registrar Cotización
def registrar_cotizacion(request, oportunidad_id=None):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    oportunidad = get_object_or_404(Oportunidad, id=oportunidad_id)
    cliente = oportunidad.cliente

    if request.method == 'POST':
        descripcion = request.POST['descripcion']
        valor = request.POST['valor']
        estado = request.POST['estado']
        cotizacion = Cotizacion.objects.create(oportunidad=oportunidad, descripcion=descripcion, valor=valor, estado=estado)
        if estado == 'aceptada':
            factura = Factura.objects.create(cliente=cliente, total=valor)
            Ingreso.objects.create(factura=factura, fecha_pago=factura.fecha_emision, monto=valor, origen='venta')
        return redirect('detalle_oportunidad', oportunidad_id=oportunidad.id)
    
    return render(request, 'chat/registrar_cotizacion.html', {'oportunidad': oportunidad, 'cliente': cliente})

# Editar Cotización
def editar_cotizacion(request, cotizacion_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    if request.method == 'POST':
        cotizacion.descripcion = request.POST['descripcion']
        cotizacion.valor = request.POST['valor']
        cotizacion.estado = request.POST['estado']
        cotizacion.save()
        return redirect('detalle_cotizacion', cotizacion_id=cotizacion.id)
    return render(request, 'chat/editar_cotizacion.html', {'cotizacion': cotizacion})

# Eliminar Cotización
def eliminar_cotizacion(request, cotizacion_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    cotizacion.delete()
    return redirect('lista_cotizaciones')


# Solicitud del Cliente
def registrar_solicitud(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        cliente_id = request.POST['cliente']
        descripcion = request.POST['descripcion']
        valor = request.POST['valor']
        cliente = get_object_or_404(Cliente, id=cliente_id)
        oportunidad = Oportunidad.objects.create(cliente=cliente, descripcion=descripcion, valor=valor, estado='prospecto')
        Cotizacion.objects.create(oportunidad=oportunidad, descripcion=descripcion, valor=valor, estado='enviada')
        return redirect('detalle_oportunidad', oportunidad_id=oportunidad.id)
    clientes = Cliente.objects.all()
    return render(request, 'chat/registrar_solicitud.html', {'clientes': clientes})

# Generar Factura desde Cotización
def generar_factura_desde_cotizacion(request, cotizacion_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    if cotizacion.estado == 'aceptada':
        if request.method == 'POST':
            tipo_pago = request.POST['tipo_pago']
            factura = Factura.objects.create(cliente=cotizacion.oportunidad.cliente, total=cotizacion.valor)
            if tipo_pago == 'total':
                Ingreso.objects.create(factura=factura, fecha_pago=factura.fecha_emision, monto=cotizacion.valor, origen='venta')
                factura.estado = 'pagada'
            else:
                # Registro inicial de cobranza parcial
                monto_inicial = request.POST['monto_inicial']
                Cobranza.objects.create(factura=factura, cliente=factura.cliente, monto=monto_inicial, estado='parcial')
                Ingreso.objects.create(factura=factura, fecha_pago=factura.fecha_emision, monto=monto_inicial, origen='cobranza')
            factura.save()
            return redirect('seguimiento_pago', factura_id=factura.id)
        return render(request, 'chat/generar_factura.html', {'cotizacion': cotizacion})
    return redirect('detalle_cotizacion', cotizacion_id=cotizacion.id)

# Generación de Factura
def generar_factura(request, oportunidad_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    oportunidad = get_object_or_404(Oportunidad, id=oportunidad_id)
    factura = Factura.objects.create(cliente=oportunidad.cliente, total=oportunidad.valor)
    return redirect('detalle_factura', factura_id=factura.id)

# Lista de Facturas
def lista_facturas(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    facturas = Factura.objects.all()
    return render(request, 'chat/lista_facturas.html', {'facturas': facturas})

# Detalle de Factura
def detalle_factura(request, factura_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    factura = get_object_or_404(Factura, id=factura_id)
    return render(request, 'chat/detalle_factura.html', {'factura': factura})

# Registro de Venta
def registrar_venta(request, factura_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    factura = get_object_or_404(Factura, id=factura_id)
    if request.method == 'POST':
        fecha_pago = request.POST['fecha_pago']
        monto = request.POST['monto']
        Ingreso.objects.create(factura=factura, fecha_pago=fecha_pago, monto=monto, origen='venta')
        factura.estado = 'pagada'
        factura.save()
        return redirect('seguimiento_pago', factura_id=factura.id)
    return render(request, 'chat/registrar_venta.html', {'factura': factura})

# Lista de Ingresos
def lista_ingresos(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    ingresos = Ingreso.objects.all()
    return render(request, 'chat/lista_ingresos.html', {'ingresos': ingresos})

# Registro de Cobranza
def registrar_cobranza(request, factura_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    factura = get_object_or_404(Factura, id=factura_id)
    if request.method == 'POST':
        form = CobranzaForm(request.POST)
        if form.is_valid():
            cobranza = form.save(commit=False)
            cobranza.factura = factura
            cobranza.cliente = factura.cliente
            cobranza.save()
            Ingreso.objects.create(factura=factura, fecha_pago=cobranza.fecha_cobranza, monto=cobranza.monto, origen='cobranza')
            return redirect('detalle_factura', factura_id=factura.id)
    else:
        form = CobranzaForm()
    return render(request, 'chat/registrar_cobranza.html', {'form': form, 'factura': factura})

def lista_cobranzas(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    cobranzas = Cobranza.objects.all()
    return render(request, 'chat/lista_cobranzas.html', {'cobranzas': cobranzas})

# Seguimiento de Pago
def seguimiento_pago(request, factura_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    factura = get_object_or_404(Factura, id=factura_id)
    cobranzas = Cobranza.objects.filter(factura=factura)
    
    if request.method == 'POST':
        monto = request.POST['monto']
        cobranza = Cobranza.objects.create(factura=factura, cliente=factura.cliente, monto=monto, estado='parcial')
        Ingreso.objects.create(factura=factura, fecha_pago=cobranza.fecha_cobranza, monto=cobranza.monto, origen='cobranza')
        
        # Actualizar el estado de la factura
        total_pagado = sum(cobranza.monto for cobranza in factura.cobranzas.all())
        if total_pagado >= factura.total:
            factura.estado = 'pagada'
        else:
            factura.estado = 'pendiente'
        factura.save()
        
        return redirect('seguimiento_pago', factura_id=factura.id)
    
    return render(request, 'chat/seguimiento_pago.html', {
        'factura': factura,
        'cobranzas': cobranzas
    })

# Actualización de Ingresos
def actualizar_ingresos(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    ingresos = Ingreso.objects.all()
    total_ingresos = sum(ingreso.monto for ingreso in ingresos)
    return render(request, 'chat/actualizar_ingresos.html', {'total_ingresos': total_ingresos})


# Registro de Consulta o Queja
def registrar_consulta(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        cliente_id = request.POST['cliente']
        descripcion = request.POST['descripcion']
        cliente = get_object_or_404(Cliente, id=cliente_id)
        Consulta.objects.create(cliente=cliente, descripcion=descripcion)
        return redirect('lista_consultas')
    clientes = Cliente.objects.all()
    return render(request, 'chat/registrar_consulta.html', {'clientes': clientes})
# Lista de Consultas
def lista_consultas(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    consultas = Consulta.objects.all()
    return render(request, 'chat/lista_consultas.html', {'consultas': consultas})
# Detalle de Consulta
def detalle_consulta(request, consulta_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    consulta = get_object_or_404(Consulta, id=consulta_id)
    return render(request, 'chat/detalle_consulta.html', {'consulta': consulta})

# Resolución del Problema
def resolver_consulta(request, consulta_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == 'POST':
        consulta.estado = 'resuelto'
        consulta.fecha_resolucion = timezone.now()
        consulta.save()
        return redirect('detalle_consulta', consulta_id=consulta.id)
    return render(request, 'chat/resolver_consulta.html', {'consulta': consulta})

# Ajuste de Facturación
def ajustar_facturacion(request, consulta_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    consulta = get_object_or_404(Consulta, id=consulta_id)
    facturas = Factura.objects.filter(cliente=consulta.cliente)
    if request.method == 'POST':
        factura_id = request.POST['factura']
        estado = request.POST['estado']
        factura = get_object_or_404(Factura, id=factura_id)
        factura.estado = estado
        factura.save()
        return redirect('detalle_consulta', consulta_id=consulta.id)
    return render(request, 'chat/ajustar_facturacion.html', {'consulta': consulta, 'facturas': facturas})

# Seguimiento al Cliente
def seguimiento_cliente(request, consulta_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    consulta = get_object_or_404(Consulta, id=consulta_id)
    return render(request, 'chat/seguimiento_cliente.html', {'consulta': consulta})

# Cierre del Caso
def cerrar_caso(request, consulta_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    consulta = get_object_or_404(Consulta, id=consulta_id)
    consulta.estado = 'cerrado'
    consulta.save()
    return redirect('lista_consultas')