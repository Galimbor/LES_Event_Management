from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Recurso, Equipamento, Servico, Espaco
from .forms import RecursoForm, EquipamentoForm, EspacoForm, ServicoForm


# Create your views here.


def recursos(request):
    obj = Recurso.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/recurso_list.html', context)

def equipamentos(request):
    obj = Equipamento.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/equip_list.html', context)

def servicos(request):
    obj = Servico.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/servico_list.html', context)

def espacos(request):
    obj = Espaco.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/espaco_list.html', context)


def recurso_create(request):
    form = RecursoForm(request.POST or None)
    if form.is_valid():
        # Evento data
        nome = request.POST.get("nome")
        fonte = request.POST.get("fonte")
        recurso = Recurso(nome=nome, fonte=fonte)
        recurso.save()
        return redirect('Recurso:recursos')
    context = {
        'form': form
    }
    return render(request, 'Recurso/recurso_create.html', context)


def recurso_detail(request, my_id):
    obj = get_object_or_404(Recurso, id=my_id)
    context = {
        'object': obj
    }
    return render(request, "Recurso/recurso_detail.html", context)


def recurso_delete(request, my_id):
    obj = get_object_or_404(Recurso, id=my_id)
    obj.delete()
    return redirect('Recurso:recursos')



def equipamento_create(request):
    form = EquipamentoForm(request.POST or None)
    if form.is_valid():
        # Evento data
        # nome = request.POST.get("nome")
        # descricao = request.POST.get("descricao")
        # reservado = request.POST.get("reservado")
        #
        # recurso = Equipamento(nome=nome, descricao=descricao, reservado=reservado, )
        form.save()
        return redirect('Recurso:equipamentos')
    context = {
        'form': form
    }
    return render(request, 'Recurso/equip_create.html', context)


def equipamento_detail(request, my_id):
    obj = get_object_or_404(Recurso, id=my_id)
    context = {
        'object': obj
    }
    return render(request, "Recurso/equip_detail.html", context)


def equipamento_delete(request, my_id):
    obj = get_object_or_404(Recurso, id=my_id)
    obj.delete()
    return redirect('Recurso:equipamentos')



def espaco_create(request):
    form = EspacoForm(request.POST or None)
    if form.is_valid():
        # # Evento data
        # nome = request.POST.get("nome")
        # fonte = request.POST.get("fonte")
        # recurso = Recurso(nome=nome, fonte=fonte)
        # recurso.save()
        form.save()
        return redirect('Recurso:espacos')
    context = {
        'form': form
    }
    return render(request, 'Recurso/espaco_create.html', context)


def espaco_detail(request, my_id):
    obj = get_object_or_404(Recurso, id=my_id)
    context = {
        'object': obj
    }
    return render(request, "Recurso/espaco_detail.html", context)


def espaco_delete(request, my_id):
    obj = get_object_or_404(Recurso, id=my_id)
    obj.delete()
    return redirect('Recurso:espacos')


def servico_create(request):
    form = ServicoForm(request.POST or None)
    if form.is_valid():
        # # Evento data
        # nome = request.POST.get("nome")
        # fonte = request.POST.get("fonte")
        # recurso = Recurso(nome=nome, fonte=fonte)
        # recurso.save()
        form.save()
        return redirect('Recurso:servicos')
    context = {
        'form': form
    }
    return render(request, 'Recurso/servico_create.html', context)


def servico_detail(request, my_id):
    obj = get_object_or_404(Recurso, id=my_id)
    context = {
        'object': obj
    }
    return render(request, "Recurso/servico_detail.html", context)


def servico_delete(request, my_id):
    obj = get_object_or_404(Recurso, id=my_id)
    obj.delete()
    return redirect('Recurso:servicos')
