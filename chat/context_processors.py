from .models import Usuario

def usuario_actual(request):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            return {'usuario_actual': usuario}
        except Usuario.DoesNotExist:
            return {}
    return {}