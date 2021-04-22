from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import EventoForm, LogisticaForm
from Neglected.models import Timedate
from .models import Evento, Logistica
from Recurso.models import Tipodeequipamento, Tipoespaco, Tiposervico
from django.urls import reverse


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


def create_event(request):
    form = EventoForm(request.POST or None)
    if form.is_valid():
        # Date and time data
        date_i = request.POST.get("data_i")
        date_f = request.POST.get("data_f")
        time_i = request.POST.get("hora_i")
        time_f = request.POST.get("hora_f")
        # Create TimeDate Obj
        horario = Timedate(datainicial=date_i, horainicial=time_i,
                           datafinal=date_f, horafinal=time_f)
        horario.save()

        # Evento data
        nome = request.POST.get("nome")
        desc = request.POST.get("descricaogeral")
        max_p = request.POST.get("maxparticipantes")
        val_insc = 1 if request.POST.get("radio") == 'sim' else 0
        # Create Evento Obj
        evento = Evento(nome=nome, descricaogeral=desc, maxparticipantes=max_p,
                        horario=horario, estado="Pendente", val_inscritos=val_insc, inscritos=0)
        evento.save()
        return redirect('Evento:eventos')
    else:
        print(form.errors)
    context = {
        'form': form
    }
    return render(request, 'Evento/criar_evento.html', context)
