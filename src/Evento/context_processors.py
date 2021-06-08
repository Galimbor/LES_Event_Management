from Utilizadores.models import User


def add_variable_to_context(request):
    tipo = None
    if request.user.is_superuser:
        return {}
    if request.user.is_authenticated:
        user_django = request.user
        user = User.objects.filter(email=user_django.email)
        id_gcp = user[0].gcpid
        id_prop_i = user[0].proponente_internoid
        id_ext_i = user[0].proponente_externoid
        id_servicos = user[0].servicostecnicosid
        tipo = None
        if id_gcp is not None:
            tipo = 'gcp'
        elif id_prop_i is not None:
            tipo = 'interno'
        elif id_ext_i is not None:
            tipo = 'externo'
        elif id_servicos is not None:
            tipo = 'servicos'

    return {
        'user_tipo': tipo,
    }