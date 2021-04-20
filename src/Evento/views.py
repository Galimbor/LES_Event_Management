from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import EventoForm
from Neglected.models import Timedate
from .models import Evento
from django.urls import reverse


# Create your views here.


def home_view(request):
    return render(request, 'inicio.html')


def eventos(request):
    #  events = Evento.objects.all().filter(estado='aceite')
    events = Evento.objects.all()  # temporary

    context = {
        'eventos': events,
    }

    return render(request, 'Evento/eventos.html', context)


def create_event2(request, event_id):
    print(event_id)
    return render(request, 'Evento/criar_evento2.html')


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
        # Create Evento Obj
        evento = Evento(nome=nome, descricaogeral=desc, maxparticipantes=max_p,
                        horario=horario, estado="Pendente")
        evento.save()
        return redirect('Evento:eventos')
    else:
        print(form.errors)
    context = {
        'form': form
    }
    return render(request, 'Evento/criar_evento.html', context)
