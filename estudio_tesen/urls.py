"""
URL configuration for estudio_tesen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from chat import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('chat/<int:usuario_id>/', views.chat, name='chat'),
    path('enviar/<int:usuario_id>/', views.enviar_mensaje, name='enviar_mensaje'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('backup/', views.backup_database, name='backup_database'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('clientes/registrar/', views.registrar_cliente, name='registrar_cliente'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/segmentados/<str:estado>/', views.lista_clientes_segmentados, name='lista_clientes_segmentados'),
    path('buscar/', views.buscar, name='buscar'),
    #api buscar clientes
    path('buscar-cliente-dni/', views.buscar_cliente_por_dni, name='buscar_cliente_por_dni'),
    #...
    path('ventas/oportunidades/', views.lista_oportunidades, name='lista_oportunidades'),
    path('ventas/oportunidades/<int:oportunidad_id>/', views.detalle_oportunidad, name='detalle_oportunidad'),
    path('ventas/oportunidades/registrar/', views.registrar_oportunidad, name='registrar_oportunidad'),
    path('ventas/oportunidades/<int:oportunidad_id>/editar/', views.editar_oportunidad, name='editar_oportunidad'),
    path('ventas/oportunidades/<int:oportunidad_id>/eliminar/', views.eliminar_oportunidad, name='eliminar_oportunidad'),
    path('ventas/cotizaciones/', views.lista_cotizaciones, name='lista_cotizaciones'),
    path('ventas/cotizaciones/<int:cotizacion_id>/', views.detalle_cotizacion, name='detalle_cotizacion'),
    path('ventas/cotizaciones/registrar/<int:oportunidad_id>/', views.registrar_cotizacion, name='registrar_cotizacion'),
    path('ventas/cotizaciones/<int:cotizacion_id>/editar/', views.editar_cotizacion, name='editar_cotizacion'),
    path('ventas/cotizaciones/<int:cotizacion_id>/eliminar/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
    path('ventas/solicitud/', views.registrar_solicitud, name='registrar_solicitud'),
    
    #facturacion
    path('ventas/factura/generar/<int:oportunidad_id>/', views.generar_factura, name='generar_factura'),
    path('cotizaciones/generar_factura/<int:cotizacion_id>/', views.generar_factura_desde_cotizacion, name='generar_factura_desde_cotizacion'),

    path('ventas/facturas/', views.lista_facturas, name='lista_facturas'),
    path('ventas/facturas/<int:factura_id>/', views.detalle_factura, name='detalle_factura'),
    path('ventas/venta/registrar/<int:factura_id>/', views.registrar_venta, name='registrar_venta'),
    path('ventas/ingresos/', views.lista_ingresos, name='lista_ingresos'),
    path('ventas/seguimiento/<int:factura_id>/', views.seguimiento_pago, name='seguimiento_pago'),
    path('ventas/ingresos/actualizar/', views.actualizar_ingresos, name='actualizar_ingresos'),
    path('atencion/consultas/', views.lista_consultas, name='lista_consultas'),
    path('atencion/consultas/registrar/', views.registrar_consulta, name='registrar_consulta'),
    path('atencion/consultas/<int:consulta_id>/', views.detalle_consulta, name='detalle_consulta'),
    path('atencion/consultas/<int:consulta_id>/resolver/', views.resolver_consulta, name='resolver_consulta'),
    path('atencion/consultas/<int:consulta_id>/ajustar/', views.ajustar_facturacion, name='ajustar_facturacion'),
    path('atencion/consultas/<int:consulta_id>/seguimiento/', views.seguimiento_cliente, name='seguimiento_cliente'),
    path('atencion/consultas/<int:consulta_id>/cerrar/', views.cerrar_caso, name='cerrar_caso'),
    path('grupos_chat/', views.lista_grupos_chat, name='lista_grupos_chat'),
    path('grupos_chat/crear/', views.crear_grupo_chat, name='crear_grupo_chat'),
    path('grupos_chat/<int:grupo_id>/', views.chat_grupo, name='chat_grupo'),
    path('grupos_chat/<int:grupo_id>/editar/', views.editar_grupo_chat, name='editar_grupo_chat'),
    path('grupos_chat/<int:grupo_id>/eliminar/', views.eliminar_grupo_chat, name='eliminar_grupo_chat'),
    path('api/clientes/', views.ClienteListCreateAPIView.as_view(), name='cliente-list-create'),
    path('api/clientes/<int:pk>/', views.ClienteRetrieveUpdateDestroyAPIView.as_view(), name='cliente-retrieve-update-destroy'),
    path('buscar_cliente_api/', views.buscar_cliente_api, name='buscar_cliente_api'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
