from django.shortcuts import render
from django.http import HttpResponse
from .models import  Evento

# Create your views here.


def home_view(*arg, **kwargs):
    return HttpResponse('<h1> Hello from MArs </h1>')


def eventos(request):

    events = Evento.objects.all().filter(estado='aceite')

    context = {
        'eventos' : events,
    }

    return render(request, 'evento/eventos.html', context)