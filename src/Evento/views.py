from django.shortcuts import redirect, render
from .forms import LogisticaForm
from Neglected.models import Timedate
from .models import Evento, Logistica, Tipoevento
from Recurso.models import Tipodeequipamento, Tipoespaco, Tiposervico
from GestorTemplates.models import Formulario, CampoFormulario, Campo


# Create your views here.


def home_view(request):
    return render(request, 'inicio.html')


def eventos(request):
    #  events = Evento.objects.all().filter(estado='aceite')
    events = Evento.objects.all()  # temporary
    logistica = Logistica.objects.all()

    context = {
        'eventos': events,
        'logistica': logistica
    }

    return render(request, 'Evento/eventos.html', context)


def meus_eventos(request):
    #  events = Evento.objects.all().filter(estado='aceite')
    events = Evento.objects.all()  # temporary
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


def gerir(request, event_id):
    context = {
        'evento': Evento.objects.get(id=event_id)
    }
    return render(request, 'Evento/gerir.html', context)


def create_event(request, type_id):
    formulario = Formulario.objects.filter(tipoeventoid=type_id, tipoformularioid=3)
    perguntas = CampoFormulario.objects.filter(formularioid=formulario[0])

    for pergunta in perguntas:
        if pergunta.campoid.tipocampoid.nome == 'RadioBox' or \
                pergunta.campoid.tipocampoid.nome == 'Dropdown':
            pergunta.campoid.respostas = pergunta.campoid.respostapossivelid.nome.split(",")

    if request.method == 'POST':
        nome = request.POST.get("10")
        desc = request.POST.get("11")
        num_p = request.POST.get("12")
        val = request.POST.get("13")
        data_i = request.POST.get("14")
        data_f = request.POST.get("15")
        hora_i = request.POST.get("16")
        hora_f = request.POST.get("17")

        if val == 'Sim':
            val = 1
        else:
            val = 0

        horario = Timedate(datainicial=data_i, datafinal=data_f, horainicial=hora_i, horafinal=hora_f)
        horario.save()
        evento = Evento(nome=nome, descricaogeral=desc, maxparticipantes=num_p, val_inscritos=val, horario=horario,
                        inscritos=0, estado="Pendente")
        evento.save()

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
