from django.shortcuts import render
from django.http import HttpResponse
from .forms import EventoForm

# Create your views here.


def home_view(request):
   return render(request, 'inicio.html')


def eventos(request):
   return render(request, 'Evento/eventos.html')

def create_event(request):
   form = EventoForm(request.POST or None)
   if form.is_valid():
      form.save()

   context = {
      'form': form
   }
   return render(request, 'Evento/criar_evento.html', context)
