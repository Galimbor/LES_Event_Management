from django.shortcuts import render
from django.http import HttpResponse
from .forms import EventoForm
from Neglected.models import Timedate
from .models import Evento

# Create your views here.


def home_view(request):
   return render(request, 'inicio.html')


def eventos(request):
   return render(request, 'Evento/eventos.html')

def create_event(request):
   form = EventoForm(request.POST or None)
   print(request.POST)
   print(form)
   if form.is_valid():
      # request.POST.get("field")
      date_i = request.POST.get("date-i")
      time_i = request.POST.get("time-i")
      date_f = request.POST.get("date-f")
      time_f = request.POST.get("time-f")
      horario = Timedate(datainicial=date_i, horainicial=time_i, datafinal=date_f, horafinal=time_f)
      horario.save()
      
      # Evento data
      nome = request.POST.get("nome")
      desc = request.POST.get("descricaogeral")
      max_p = request.POST.get("maxparticipantes")
      evento = Evento(nome=nome, descricaogeral=desc, maxparticipantes=max_p, horario=horario, estado="Pendente")
      evento.save()
   else:
      print("not valid!")

   context = {
      'form': form
   }
   return render(request, 'Evento/criar_evento.html', context)
