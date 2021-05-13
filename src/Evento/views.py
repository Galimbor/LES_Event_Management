from django.shortcuts import redirect, render
from Neglected.models import Timedate
from .models import Evento, Logistica, Tipoevento
from Recurso.models import Tipodeequipamento, Tipoespaco, Tiposervico
from GestorTemplates.models import Formulario, CampoFormulario, Campo, Resposta
from Utilizadores.models import User
from django.db.models import Q


# Homepage.
def home_view(request):
    return render(request, 'inicio.html')


# Show all the events that has the final validation.
def eventos(request):
    events = Evento.objects.filter(estado='Aceite')
    logistica = Logistica.objects.all()

    context = {
        'eventos': events,
        'logistica': logistica
    }

    return render(request, 'Evento/eventos.html', context)


# Show all the events that as been created so GCP users can manage it.
# Only GCP user will have access.
def eventos_gerir(request):
    #  events = Evento.objects.all().filter(estado='aceite')
    events = Evento.objects.all()  # temporary
    logistica = Logistica.objects.all()

    context = {
        'eventos': events,
        'logistica': logistica,
    }

    return render(request, 'Evento/eventos_gerir.html', context)


# Show events created by the current user.
def meus_eventos(request):
    # Get current user
    user = get_user(request)

    # Get user type
    id_gcp = user[0].gcpid
    id_prop_i = user[0].proponente_internoid
    id_ext_i = user[0].proponente_externoid

    # Get events created by current user
    # TODO: change filter.
    events = Evento.objects.filter(proponente_externoid=id_ext_i, proponente_internoid=id_prop_i)  # temporary
    logistica = Logistica.objects.all()

    context = {
        'eventos': events,
        'logistica': logistica
    }
    return render(request, 'Evento/meus_eventos.html', context)


# Give the user the option to choose which type of logistic the user wants to create to the given event.
def create_logistic(request, event_id):
    evento = Evento.objects.get(id=event_id)
    logistica = Logistica.objects.filter(eventoid=evento)
    if not logistica:
        new_logista = Logistica(nome=f'logistica-{evento.id}', eventoid=evento)
        new_logista.save()

    context = {
        'evento': evento,
    }
    return render(request, 'Evento/criar_logistica.html', context)


# Equipament Logistic
def equip_logistic(request, event_id):
    equip = Tipodeequipamento()
    return render_logistic_form_by_type(request, event_id, equip, 1)


# Espaco Logistic
def espaco_logistic(request, event_id):
    espaco = Tipoespaco()
    return render_logistic_form_by_type(request, event_id, espaco, 2)


# Servico Logistic
def servico_logistic(request, event_id):
    servico = Tiposervico()
    return render_logistic_form_by_type(request, event_id, servico, 3)


# Submit logistic to the GCP
def submit_logistic(request, event_id):
    evento = Evento.objects.get(id=event_id)
    evento.estado = 'Logistica Pendente'
    evento.save()
    return redirect('Evento:meus-eventos')


# Return page to manage the given event
def gerir(request, event_id):
    context = {
        'evento': Evento.objects.get(id=event_id),
        'id': event_id
    }
    return render(request, 'Evento/gerir.html', context)


# Create an event after the form is submitted
def create_event(request, type_id):
    user = get_user(request)
    tipo = get_user_type(request)
    id_gcp = user[0].gcpid
    id_prop_i = user[0].proponente_internoid
    id_ext_i = user[0].proponente_externoid

    formulario = Formulario.objects.filter(tipoeventoid=type_id, tipoformularioid=3)
    perguntas = CampoFormulario.objects.filter(formularioid=formulario[0]).exclude(Q(campoid_id=22) | Q(campoid_id=23))

    for pergunta in perguntas:
        if pergunta.campoid.tipocampoid.nome == 'Escolha Múltipla' or \
                pergunta.campoid.tipocampoid.nome == 'Dropdown':
            pergunta.campoid.respostas = pergunta.campoid.respostapossivelid.nome.split(",")

    evento = Evento()
    horario = Timedate()
    respostas = []

    if request.method == 'POST':
        for pergunta in perguntas:
            id = pergunta.campoid.id
            if id == 10:
                nome = request.POST.get(f'{id}')
                evento.nome = nome
            elif id == 11:
                desc = request.POST.get(f'{id}')
                evento.descricaogeral = desc
            elif id == 12:
                num_p = request.POST.get(f'{id}')
                evento.maxparticipantes = num_p
            elif id == 31:
                val = request.POST.get(f'{id}')
                if val == 'Sim':
                    val = 1
                else:
                    val = 0
                evento.val_inscritos = val
            elif id == 14:
                data_i = request.POST.get(f'{id}')
                horario.datainicial = data_i
            elif id == 15:
                data_f = request.POST.get(f'{id}')
                horario.datafinal = data_f
            elif id == 16:
                hora_i = request.POST.get(f'{id}')
                horario.horainicial = hora_i
            elif id == 17:
                hora_f = request.POST.get(f'{id}')
                horario.horafinal = hora_f
            resposta = Resposta(conteudo=request.POST.get(f'{id}'), campoid=pergunta.campoid, eventoid=evento)
            respostas.append(resposta)

        horario.save()
        evento.inscritos = 0
        evento.estado = "Validado"
        evento.proponente_internoid = id_prop_i
        evento.proponente_externoid = id_ext_i
        evento.horario = horario
        # TODO: gcp id

        evento.save()

        for resp in respostas:
            resp.save()

        resposta_estado = Resposta(conteudo='Pendente', campoid_id=32, eventoid=evento)
        resposta_estado.save()
        resposta_inscritos = Resposta(conteudo=0, campoid_id=23, eventoid=evento)
        resposta_inscritos.save()
        # Redirect to eventos page
        return redirect('Evento:eventos')


    context = {
        'campos': perguntas
    }
    return render(request, 'Evento/criar_evento.html', context)


def select_type(request):
    tipos = Tipoevento.objects.all()

    if request.method == 'POST':
        tipo = request.POST['radio']
        return redirect('Evento:create-event', tipo)

    context = {
        'tipos': tipos
    }
    return render(request, 'Evento/selecionar_tipo.html', context)


# View Logisticas
def view_logisticas(request, event_id):
    evento = Evento.objects.get(id=event_id)
    logistica = Logistica.objects.get(eventoid=evento)
    logistica_equipamento = Tipodeequipamento.objects.filter(logisticaid=logistica)
    logistica_servico = Tiposervico.objects.filter(logisticaid=logistica)
    logistica_espaco = Tipoespaco.objects.filter(logisticaid=logistica)

    context = {
        'equipamentos': logistica_equipamento,
        'servicos': logistica_servico,
        'espacos': logistica_espaco,
        'evento': evento,
    }
    return render(request, 'Evento/view_logistica.html', context)


# View a specific event
def view_event(request, event_id):
    evento = Evento.objects.get(id=event_id)

    horario = Timedate.objects.get(id=evento.horario.id)

    context = {
        'evento': evento,
        'data_i': horario.datainicial,
        'data_f': horario.datafinal,
        'hora_i': horario.horainicial,
        'hora_f': horario.horafinal,
    }
    return render(request, 'Evento/view_evento.html', context)





# HELPER FUNCTIONS
def get_user_type(request):
    user_django = request.user
    user = User.objects.filter(email=user_django.email)
    if user[0].gcpid is not None:
        tipo = 'gcp'
    elif user[0].proponente_internoid is not None:
        tipo = 'interno'
    elif user[0].proponente_externoidid is not None:
        tipo = 'externo'
    elif user[0].servicostecnicosid is not None:
        tipo = 'servicos'
    else:
        tipo = None
    return tipo


def get_user(request):
    user_django = request.user
    user = User.objects.filter(email=user_django.email)
    return user


def render_logistic_form_by_type(request, event_id, obj, type_logistic):
    # Event.
    evento = Evento.objects.get(id=event_id)

    # Logistic
    logistic = Logistica.objects.filter(eventoid=evento)

    # Retrieve equip logistic form for the given event.
    formulario = Formulario.objects.filter(tipoformularioid=4)
    perguntas = CampoFormulario.objects.filter(formularioid=formulario[0])

    # Get multiple choices and bind to the pergunta obj
    for pergunta in perguntas:
        if pergunta.campoid.tipocampoid.nome == 'Escolha Múltipla' or \
                pergunta.campoid.tipocampoid.nome == 'Dropdown':
            pergunta.campoid.respostas = pergunta.campoid.respostapossivelid.nome.split(",")

    horario = Timedate()

    if request.method == 'POST':
        get_data_from_form(request, obj, perguntas, horario, logistic[0], evento)

        # Redirect to eventos page
        return redirect('Evento:meus-eventos')
    else:
        context = {
            'evento': evento,
            'campos': perguntas
        }
        if type_logistic == 1:
            return render(request, 'Evento/equipamento_logistica.html', context)
        elif type_logistic == 2:
            return render(request, 'Evento/espaco_logistica.html', context)
        elif type_logistic == 3:
            return render(request, 'Evento/servico_logistica.html', context)
        else:
            return render(request, 'Evento/eventos.html', context)


def get_data_from_form(request, tipo, perguntas, horario, logistica, evento):
    for pergunta in perguntas:
        id_p = pergunta.campoid.id
        if id_p == 11:
            desc = request.POST.get(f'{id_p}')
            tipo.nome = desc
        elif id_p == 14:
            data_i = request.POST.get(f'{id_p}')
            horario.datainicial = data_i
        elif id_p == 15:
            data_f = request.POST.get(f'{id_p}')
            horario.datafinal = data_f
        elif id_p == 16:
            hora_i = request.POST.get(f'{id_p}')
            horario.horainicial = hora_i
        elif id_p == 17:
            hora_f = request.POST.get(f'{id_p}')
            horario.horafinal = hora_f
        elif id_p == 24:
            quantidade = request.POST.get(f'{id_p}')
            tipo.quantidade = quantidade
        resposta = Resposta(conteudo=request.POST.get(f'{id_p}'), campoid=pergunta.campoid, eventoid=evento)
        resposta.save()

    horario.save()
    tipo.horariorequisicao = horario
    tipo.logisticaid = logistica
    tipo.save()
