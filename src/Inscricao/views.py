from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import InscricaoForm
from Evento.models import Evento
from .models import Inscricao

from django.contrib import messages


# Create your views here.

def create_inscricao(request, eventoid):
    form = InscricaoForm(request.POST or None)

    if form.is_valid():
        eventoid = Evento.objects.get(id=eventoid)

        # We don't have users implemented yet.
        # if request.user.is_authenticated:
        #     userid = request.user
        # We don't have users yet.
        # if not Inscricao.objects.filter(userid=userid).filter(eventoid=eventoid):
        #     if True:
        #         messages.error(request, f'Já se encontra inscrito no evento.')
        #         return redirect('Evento:list_eventos')

        nome = form.cleaned_data.get('nome')
        email = form.cleaned_data.get('email')
        idade = form.cleaned_data.get('idade')
        telemovel = form.cleaned_data.get('telemovel')
        profissao = form.cleaned_data.get('profissao')

        userid = None

        inscricao = Inscricao(nome=nome, email=email, idade=idade, telemovel=telemovel, profissao=profissao,
                              eventoid=eventoid, userid=userid)

        inscricao.save()

        messages.success(request, f'Inscreveu-se com sucesso no evento.')

        return redirect('Evento:list_eventos')

    context = {
        'form': form
    }
    return render(request, 'inscricao/inscricao_create.html', context)
