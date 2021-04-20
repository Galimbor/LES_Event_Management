from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def home_view(request):
   return render(request, 'inicio.html')


def eventos(request):
   return render(request, 'Evento/eventos.html')

def create_event(request):
   return render(request, 'Evento/criar_evento.html')
