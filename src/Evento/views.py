from django.shortcuts import render
from django.http import HttpResponse
from .models import  Evento

# Create your views here.



def eventos(request):

    events = Evento.objects.all().filter(estado='aceite')

    context = {
        'eventos' : events,
    }

    return render(request, 'evento/participante/eventos.html', context)


