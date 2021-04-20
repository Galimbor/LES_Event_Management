from django.shortcuts import render
from django.http import HttpResponse
from .forms import InscricaoForm


# Create your views here.

def create_inscricao(request):
    form = InscricaoForm(request.POST or None)

    if form.is_valid():
        print("I'M HERE")
        # form.save()

    context = {
        'form': form
    }
    return render(request, 'inscricao/inscricao_create.html', context)
