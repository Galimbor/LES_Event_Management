from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib import messages
from .models import Evento, Recurso, Equipamento, Servico, Espaco, Empresa, Edificio, Unidadeorganica, Campus, \
    Universidade, EventoRecurso, Componente, TimedateRecurso
from .forms import RecursoForm, EquipamentoForm, EspacoForm, ServicoForm, EmpresaForm, EdificioForm, CampusForm, \
    UniversidadeForm, UnidadeOrganicaForm
from Neglected.models import Timedate

import json
from django.http import HttpResponse
from django.http import JsonResponse


# Create your views here.


def home_view(request):
    return render(request, 'inicio.html')


def recursos(request):
    obj = Recurso.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/recurso_list.html', context)

def recurso_atribuir_list(request, my_id, tipo, time):
    evento = Evento.objects.get(id=my_id)
    recursos = Recurso.objects.all()
    hora = Timedate.objects.get(id=time)

    timedates = TimedateRecurso.objects.all()

    rec_espacos = []
    rec_equipamentos = []
    rec_servicos = []


    for item in recursos:
        if item.espacoid is not None:
            flag = True
            for time in timedates:
                if (hora.datainicial >= time.timedateid.datainicial and time.timedateid.datafinal <= hora.datafinal) and (hora.horainicial >= time.timedateid.horainicial and time.timedateid.horafinal <= hora.horafinal) and (item == time.recursoid):
                    flag = False 
                    break

            if flag == True:
                rec_espacos.append(item)


        elif item.equipamentoid is not None:
            flag = True
            for time in timedates:
                if (hora.datainicial >= time.timedateid.datainicial and time.timedateid.datafinal <= hora.datafinal) and (hora.horainicial >= time.timedateid.horainicial and time.timedateid.horafinal <= hora.horafinal) and (item == time.recursoid):
                    flag = False 
                    break

            if flag == True:
                rec_equipamentos.append(item)
        elif item.servicoid is not None:
            flag = True
            for time in timedates:
                if (hora.datainicial >= time.timedateid.datainicial and time.timedateid.datafinal <= hora.datafinal) and (hora.horainicial >= time.timedateid.horainicial and time.timedateid.horafinal <= hora.horafinal) and (item == time.recursoid):
                    flag = False 
                    break

            if flag == True:
                rec_servicos.append(item) 
            

    if tipo == 'espaco':
        context = {
            "rec": rec_espacos,
            "evento": evento,
            "hora": hora
            }
    elif tipo == 'servico':
        context = {
            "rec": rec_servicos,
            "evento": evento,
            "hora": hora
            }
    elif tipo == 'equipamento':
        context = {
            "rec": rec_equipamentos,
            "evento": evento,
            "hora": hora
            }
    else:
        context = {

        }
    
    return render(request, 'Recurso/recurso_atribuir.html', context)



def recurso_atribuir(request, my_id, obj_id, time):
    evento = Evento.objects.get(id=my_id)
    recurso = Recurso.objects.get(id=obj_id)
    hora = Timedate.objects.get(id=time)

    rec_ev = EventoRecurso(eventoid=evento, recursoid=recurso)
    rec_ev.save()

    hora_rec = TimedateRecurso(recursoid=recurso, timedateid=hora)
    hora_rec.save()
    

    return redirect("Evento:view-logistic", my_id)

def recurso_atribuir_cancelar(request, my_id, obj_id):
    evento = Evento.objects.get(id=my_id)
    recurso = Recurso.objects.get(id=obj_id)

    rec_ev = EventoRecurso.objects.get(eventoid=evento, recursoid=recurso)
    rec_ev.delete()

    return redirect("Recurso:recursos-2", my_id)



def componentes(request):
    obj = Componente.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/componentes_list.html', context)


def componente_update(request, my_id):
    obj = get_object_or_404(Componente, id=my_id)
    if obj.empresaid is not None:
        return redirect('Recurso:empresa-update', obj.empresaid.id)
    elif obj.edificioid is not None:
        return redirect('Recurso:edificio-update', obj.edificioid.id)
    elif obj.campusid is not None:
        return redirect('Recurso:campus-update', obj.campusid.id)
    elif obj.universidadeid is not None:
        return redirect('Recurso:universidade-update', obj.universidadeid.id)
    else:
        return redirect('Recurso:unidade-organica-update', obj.unidade_organicaid.id)


def componente_detail(request, my_id):
    obj = get_object_or_404(Componente, id=my_id)
    if obj.empresaid is not None:
        return redirect('Recurso:empresa-detail', obj.empresaid.id)
    elif obj.edificioid is not None:
        return redirect('Recurso:edificio-detail', obj.edificioid.id)
    elif obj.campusid is not None:
        return redirect('Recurso:campus-detail', obj.campusid.id)
    elif obj.universidadeid is not None:
        return redirect('Recurso:universidade-detail', obj.universidadeid.id)
    else:
        return redirect('Recurso:unidade-organica-detail', obj.unidade_organicaid.id)


def componente_delete(request, my_id):
    obj = get_object_or_404(Componente, id=my_id)
    if obj.empresaid is not None:
        return redirect('Recurso:empresa-delete', obj.empresaid)
    elif obj.edificioid is not None:
        return redirect('Recurso:edificio-delete', obj.edificioid)
    elif obj.universidadeid is not None:
        return redirect('Recurso:universidade-delete', obj.universidadeid)
    elif obj.unidade_organicaid is not None:
        return redirect('Recurso:unidade-organica-delete', obj.unidade_organicaid)
    else:
        return redirect('Recurso:campus-delete', obj.campusid)


def recursosv2(request, my_id):
    obj = get_object_or_404(Evento, id=my_id)
    evento = Evento.objects.get(id=my_id)
    eventoRecursos = EventoRecurso.objects.filter(eventoid__id=obj.id)
    recursos = []
    for i in eventoRecursos:
        recursos.append(i.recursoid)
    context = {
        'object': recursos,
        'evento': evento
    }
    return render(request, 'Recurso/recurso_list_event.html', context)


def recurso_detail(request, my_id):
    obj = get_object_or_404(Recurso, id=my_id)

    if obj.espacoid is not None:
        return redirect('Recurso:espaco-detail', obj.espacoid.id)
    elif obj.equipamentoid is not None:
        return redirect('Recurso:equipamento-detail', obj.equipamentoid.id)
    else:
        return redirect('Recurso:servico-detail', obj.servicoid.id)


def recurso_update(request, my_id):
    obj = get_object_or_404(Recurso, id=my_id)
    if obj.espacoid is not None:
        return redirect('Recurso:espaco-update', obj.espacoid.id)
    elif obj.equipamentoid is not None:
        return redirect('Recurso:equipamento-update', obj.equipamentoid.id)
    else:
        return redirect('Recurso:servico-update', obj.servicoid.id)


def recurso_delete(request, my_id):
    obj = get_object_or_404(Recurso, id=my_id)
    if obj.espacoid is not None:
        innerObj = obj.espacoid
    elif obj.equipamentoid is not None:
        innerObj = obj.equipamentoid
    else:
        innerObj = obj.servicoid
    eventoRecursos = EventoRecurso.objects.filter(recursoid_id=obj.id)
    for i in eventoRecursos:
        i.delete()
    obj.delete()
    innerObj.delete()
    return redirect('Recurso:recursos')


def equipamentos(request):
    obj = Equipamento.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/equip_list.html', context)


def equipamento_create(request):
    form = EquipamentoForm(request.POST or None)
    form2 = RecursoForm(request.POST or None)
    if form.is_valid():
        form.save()
        empresa = request.POST.get('empresaid')
        if empresa is not None:
            fonte = 'Externa'
            recurso = Recurso(nome=request.POST.get("nome"), fonte=fonte, equipamentoid=form.instance)
        else:
            fonte = 'Interna'
            recurso = Recurso(nome=request.POST.get("nome"), fonte=fonte, empresaid=empresa,
                              equipamentoid=form.instance)
        recurso.save()
        messages.success(request, 'Equipamento criado com sucesso')
        return redirect('Recurso:recursos')
    context = {
        'form': form,
        'form2': form2
    }
    return render(request, 'Recurso/equip_create.html', context)


def equipamento_update(request, my_id):
    obj = get_object_or_404(Equipamento, id=my_id)
    form = EquipamentoForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("Recurso:recursos")
    context = {
        'form': form,
        'detail': 1
    }
    return render(request, "Recurso/equip_create.html", context)


def equipamento_detail(request, my_id):
    obj = get_object_or_404(Equipamento, id=my_id)
    context = {
        'obj': obj,
    }
    return render(request, "Recurso/equip_detail.html", context)


def equipamento_delete(request, my_id):
    obj = get_object_or_404(Equipamento, id=my_id)
    obj.delete()
    return redirect('Recurso:recursos')


def espacos(request):
    obj = Espaco.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/espaco_list.html', context)


def espaco_create(request):
    form = EspacoForm(request.POST or None)
    if form.is_valid():
        form.save()
        recurso = Recurso(nome=request.POST.get("nome"), fonte='Interna', espacoid=form.instance)
        recurso.save()
        messages.success(request, 'Espaço criado com sucesso')
        return redirect('Recurso:recursos')
    else:
        print(form.errors)
    context = {
        'form': form
    }
    return render(request, 'Recurso/espaco_create.html', context)


def espaco_update(request, my_id):
    obj = get_object_or_404(Espaco, id=my_id)
    form = EspacoForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("Recurso:recursos")
    context = {
        'form': form,
        'detail': 1
    }
    return render(request, "Recurso/espaco_create.html", context)


def espaco_detail(request, my_id):
    obj = get_object_or_404(Espaco, id=my_id)
    context = {
        'obj': obj,
    }
    return render(request, "Recurso/espaco_detail.html", context)


def espaco_delete(request, my_id):
    obj = get_object_or_404(Recurso, id=my_id)
    obj.delete()
    return redirect('Recurso:recursos')


def servicos(request):
    obj = Servico.objects.all()
    context = {
        'object': obj,
    }
    return render(request, 'Recurso/recurso_list.html', context)


def servico_create(request):
    form = ServicoForm(request.POST or None)
    form2 = RecursoForm(request.POST or None)
    if form.is_valid():
        form.save()
        empresa = request.POST.get('empresaid')
        if empresa is not None:
            fonte = 'Externa'
        else:
            fonte = 'Interna'
        recurso = Recurso(nome=request.POST.get("nome"), fonte=fonte, servicoid=form.instance)
        recurso.save()
        messages.success(request, 'Serviço criado com sucesso')
        return redirect('Recurso:recursos')
    context = {
        'form': form,
        'form2': form2
    }
    return render(request, 'Recurso/servico_create.html', context)


def servico_update(request, my_id):
    obj = get_object_or_404(Servico, id=my_id)
    form = ServicoForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("Recurso:recursos")
    context = {
        'form': form,
        'detail': 1
    }
    return render(request, "Recurso/servico_create.html", context)


def servico_detail(request, my_id):
    obj = get_object_or_404(Servico, id=my_id)
    context = {
        'obj': obj,
    }
    return render(request, "Recurso/servico_detail.html", context)


def servico_delete(request, my_id):
    obj = get_object_or_404(Servico, id=my_id)
    obj.delete()
    return redirect('Recurso:servicos')


def empresas(request):
    obj = Empresa.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/empresa_list.html', context)


def empresa_create(request):
    form = EmpresaForm(request.POST or None)
    if form.is_valid():
        form.save()
        recurso = Componente(nome=request.POST.get("nome"), empresaid=form.instance)
        recurso.save()
        messages.success(request, 'Empresa criada com sucesso')
        return redirect('Recurso:componentes')
    context = {
        'form': form,
    }
    return render(request, 'Recurso/empresa_create.html', context)


def empresa_delete(request, my_id):
    obj = get_object_or_404(Empresa, id=my_id)
    obj.delete()
    return redirect('Recurso:componentes')


def empresa_update(request, my_id):
    obj = get_object_or_404(Empresa, id=my_id)
    form = EmpresaForm(request.POST or None, instance=obj)
    print(form.fields)
    if form.is_valid():
        form.save()
    context = {
        'form': form,
        'detail': 1
    }
    return render(request, "Recurso/empresa_create.html", context)


def empresa_detail(request, my_id):
    obj = get_object_or_404(Empresa, id=my_id)
    context = {
        'obj': obj,
    }
    return render(request, "Recurso/empresa_detail.html", context)


def edificios(request):
    obj = Edificio.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/edificio_list.html', context)


def edificio_create(request):
    form = EdificioForm(request.POST or None)
    if form.is_valid():
        form.save()
        componente = Componente(nome=request.POST.get("nome"), edificioid=form.instance)
        componente.save()
        messages.success(request, 'Edifício criado com sucesso')
        return redirect('Recurso:componentes')
    context = {
        'form': form,
    }
    return render(request, 'Recurso/edificio_create.html', context)


def edificio_delete(request, my_id):
    obj = get_object_or_404(Edificio, id=my_id)
    obj.delete()
    return redirect('Recurso:edificios')


def edificio_update(request, my_id):
    obj = get_object_or_404(Edificio, id=my_id)
    form = EdificioForm(request.POST or None, instance=obj)
    print(form.fields)
    if form.is_valid():
        form.save()
    context = {
        'form': form,
        'detail': 1
    }
    return render(request, "Recurso/edificio_create.html", context)


def edificio_detail(request, my_id):
    obj = get_object_or_404(Edificio, id=my_id)
    context = {
        'obj': obj,
    }
    return render(request, "Recurso/edificio_detail.html", context)


def unidadesorganicas(request):
    obj = Unidadeorganica.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/unidade-organica_list.html', context)


def unidadeorganica_create(request):
    form = UnidadeOrganicaForm(request.POST or None)
    if form.is_valid():
        form.save()
        componente = Componente(nome=request.POST.get("nome"), unidade_organicaid=form.instance)
        componente.save()
        messages.success(request, 'Unidade Orgânica criada com sucesso')
        return redirect('Recurso:componentes')
    context = {
        'form': form,
    }
    return render(request, 'Recurso/unidade-organica_create.html', context)


def unidadeorganica_delete(request, my_id):
    obj = get_object_or_404(Unidadeorganica, id=my_id)
    obj.delete()
    return redirect('Recurso:unidades-organicas')


def unidadeorganica_update(request, my_id):
    obj = get_object_or_404(Unidadeorganica, id=my_id)
    form = UnidadeOrganicaForm(request.POST or None, instance=obj)
    print(form.fields)
    if form.is_valid():
        form.save()
    context = {
        'form': form,
        'detail': 1
    }
    return render(request, "Recurso/unidade-organica_create.html", context)


def unidadeorganica_detail(request, my_id):
    obj = get_object_or_404(Unidadeorganica, id=my_id)
    context = {
        'obj': obj,
    }
    return render(request, "Recurso/unidade-organica_detail.html", context)


def universidades(request):
    obj = Universidade.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/universidade_list.html', context)


def universidade_create(request):
    form = UniversidadeForm(request.POST or None)
    if form.is_valid():
        form.save()
        componente = Componente(nome=request.POST.get("nome"), universidadeid=form.instance)
        componente.save()
        messages.success(request, 'Universidade criada com sucesso')
        return redirect('Recurso:componentes')
    context = {
        'form': form,
    }
    return render(request, 'Recurso/universidade_create.html', context)


def universidade_update(request, my_id):
    obj = get_object_or_404(Universidade, id=my_id)
    form = UniversidadeForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    context = {
        'form': form,
        'detail': 1
    }
    return render(request, "Recurso/universidade_create.html", context)


def universidade_detail(request, my_id):
    obj = get_object_or_404(Universidade, id=my_id)
    context = {
        'obj': obj,
    }
    return render(request, "Recurso/universidade_detail.html", context)


def universidade_delete(request, my_id):
    obj = get_object_or_404(Universidade, id=my_id)
    obj.delete()
    return redirect('Recurso:universidades')


def campis(request):
    obj = Campus.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/campus_list.html', context)


def campus_create(request):
    form = CampusForm(request.POST or None)
    if form.is_valid():
        form.save()
        componente = Componente(nome=request.POST.get("nome"), campusid=form.instance)
        componente.save()
        messages.success(request, 'Campus criado com sucesso')
        return redirect('Recurso:componentes')
    context = {
        'form': form,
    }
    return render(request, 'Recurso/campus_create.html', context)


def campus_update(request, my_id):
    obj = get_object_or_404(Campus, id=my_id)
    form = CampusForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    context = {
        'form': form,
        'detail': 1
    }
    return render(request, "Recurso/campus_create.html", context)


def campus_detail(request, my_id):
    obj = get_object_or_404(Campus, id=my_id)
    context = {
        'obj': obj,
    }
    return render(request, "Recurso/campus_detail.html", context)


def campus_delete(request, my_id):
    obj = get_object_or_404(Campus, id=my_id)
    obj.delete()
    return redirect('Recurso:campis')
