from django.shortcuts import redirect, render
from .forms import LogisticaForm
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


def create_event2(request, event_id):
    evento = Evento.objects.get(id=event_id)
    form = LogisticaForm(request.POST or None)
    if form.is_valid():
        nome = request.POST.get("nome")
        quantidade = request.POST.get("quantidade")
        tipo = request.POST.get("logistica")

        # Date and time data
        date_i = request.POST.get("data_i")
        date_f = request.POST.get("data_f")
        time_i = request.POST.get("hora_i")
        time_f = request.POST.get("hora_f")
        # Create TimeDate Obj
        horario = Timedate(datainicial=date_i, horainicial=time_i,
                           datafinal=date_f, horafinal=time_f)
        horario.save()

        # Create Logistica and TipoLogistica
        logistica = Logistica(nome=nome, eventoid=evento)
        logistica.save()
        if tipo == "equipamento":
            tipo_equipamento = Tipodeequipamento(nome=nome, quantidade=quantidade, logisticaid=logistica,
                                                 horariorequisicao=horario)
            tipo_equipamento.save()
        elif tipo == "servico":
            tipo_servico = Tiposervico(nome=nome, quantidade=quantidade, logisticaid=logistica,
                                       horariorequisicao=horario)
            tipo_servico.save()
        elif tipo == "espaco":
            tipo_espaco = Tipoespaco(nome=nome, quantidade=quantidade, logisticaid=logistica,
                                     horariorequisicao=horario)
            tipo_espaco.save()
        else:
            exit(0)

        # Update Evento obj state
        evento.estado = 'Logistica Pendente'
        evento.save()

        # Redirect to eventos page
        return redirect('Evento:eventos')

    else:
        print("Not Valid!")
    context = {
        'evento': evento,
        'form': form
    }
    return render(request, 'Evento/criar_evento2.html', context)


# Return page to manage the given event
def gerir(request, event_id):
    context = {
        'evento': Evento.objects.get(id=event_id)
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
        if pergunta.campoid.tipocampoid.nome == 'RadioBox' or \
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
            elif id == 13:
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
            print(resp)
            resp.save()

        resposta_estado = Resposta(conteudo='Validado', campoid_id=22, eventoid=evento)
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