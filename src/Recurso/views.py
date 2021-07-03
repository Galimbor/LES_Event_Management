from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy

from django.contrib import messages
from .models import Evento, Recurso, Equipamento, Servico, Espaco, Empresa, Edificio, Unidadeorganica, Campus, \
    Universidade, EventoRecurso, Componente, TimedateRecurso, Tipodeequipamento, Tipoespaco, Tiposervico
from .forms import RecursoForm, EquipamentoForm, EspacoForm, ServicoForm, EmpresaForm, EdificioForm, CampusForm, \
    UniversidadeForm, UnidadeOrganicaForm
from Neglected.models import Timedate

import json
from django.http import HttpResponse
from django.http import JsonResponse


# Create your views here.


def recurso_ajax(request):
    if request.method == "GET":
        recurso_id = request.GET["id"]

        recurso = Recurso.objects.get(id=int(recurso_id))
        print(recurso)

        event_rec = EventoRecurso.objects.filter(recursoid=recurso)
        if not event_rec:
            safe_to_delete = 'true'
        else:
            safe_to_delete = 'false'

        data = {
            "res": safe_to_delete
        }
        return JsonResponse(data)


def home_view(request):
    return render(request, 'inicio.html')


def recursos(request):
    obj = Recurso.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/recurso_list.html', context)


def recurso_atribuir_list(request, my_id, tipo, time, log):
    print(log)
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
                if (
                        hora.datainicial >= time.timedateid.datainicial and time.timedateid.datafinal <= hora.datafinal) and (
                        hora.horainicial >= time.timedateid.horainicial and time.timedateid.horafinal <= hora.horafinal) and (
                        item == time.recursoid):
                    flag = False
                    break

            if flag:
                rec_espacos.append(item)

        elif item.equipamentoid is not None:
            flag = True
            for time in timedates:
                if (
                        hora.datainicial >= time.timedateid.datainicial and time.timedateid.datafinal <= hora.datafinal) and (
                        hora.horainicial >= time.timedateid.horainicial and time.timedateid.horafinal <= hora.horafinal) and (
                        item == time.recursoid):
                    flag = False
                    break

            if flag:
                rec_equipamentos.append(item)

        elif item.servicoid is not None:
            flag = True
            for time in timedates:
                if (
                        hora.datainicial >= time.timedateid.datainicial and time.timedateid.datafinal <= hora.datafinal) and (
                        hora.horainicial >= time.timedateid.horainicial and time.timedateid.horafinal <= hora.horafinal) and (
                        item == time.recursoid):
                    flag = False
                    break

            if flag:
                rec_servicos.append(item)
        else:
            logistica = None

    if tipo == 'espaco':
        print(log)
        logistica = Tipoespaco.objects.get(id=log)
        context = {
            "rec": rec_espacos,
            "evento": evento,
            "hora": hora,
            "logistica": logistica
        }
    elif tipo == 'servico':
        logistica = Tiposervico.objects.get(id=log)
        context = {
            "rec": rec_servicos,
            "evento": evento,
            "hora": hora,
            "logistica": logistica
        }
    elif tipo == 'equipamento':
        logistica = Tipodeequipamento.objects.get(id=log)
        context = {
            "rec": rec_equipamentos,
            "evento": evento,
            "hora": hora,
            "logistica": logistica
        }
    else:
        context = {

        }

    return render(request, 'Recurso/recurso_atribuir.html', context)


def recurso_atribuir(request, my_id, obj_id, time, log):
    evento = Evento.objects.get(id=my_id)
    recurso = Recurso.objects.get(id=obj_id)
    hora = Timedate.objects.get(id=time)

    rec_ev = EventoRecurso(eventoid=evento, recursoid=recurso)
    rec_ev.save()

    hora_rec = TimedateRecurso(recursoid=recurso, timedateid=hora)
    hora_rec.save()

    if recurso.espacoid is not None:
        log_esp = Tipoespaco.objects.get(id=log)
        log_esp.isAttributed = 1
        log_esp.save()

    if recurso.servicoid is not None:
        log_esp = Tiposervico.objects.get(id=log)
        log_esp.isAttributed = 1
        log_esp.save()

    if recurso.equipamentoid is not None:
        log_esp = Tipodeequipamento.objects.get(id=log)
        log_esp.isAttributed = 1
        log_esp.save()

    messages.success(request, 'Recurso atribuido com sucesso.')
    return redirect("Evento:view-logistic", my_id)


def recurso_atribuir_cancelar(request, my_id, obj_id, time):
    evento = Evento.objects.get(id=my_id)
    recurso = Recurso.objects.get(id=obj_id)

    rec_ev = EventoRecurso.objects.get(eventoid=evento, recursoid=recurso)
    rec_date = TimedateRecurso.objects.filter(recursoid=recurso, timedateid=time)
    print(rec_date)
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
        return redirect('Recurso:empresa-delete', obj.empresaid.id)
    elif obj.edificioid is not None:
        return redirect('Recurso:edificio-delete', obj.edificioid.id)
    elif obj.universidadeid is not None:
        return redirect('Recurso:universidade-delete', obj.universidadeid.id)
    elif obj.unidade_organicaid is not None:
        return redirect('Recurso:unidade-organica-delete', obj.unidade_organicaid.id)
    else:
        return redirect('Recurso:campus-delete', obj.campusid)


def recursosv2(request, my_id):
    obj = get_object_or_404(Evento, id=my_id)
    eventoRecursos = EventoRecurso.objects.filter(eventoid__id=obj.id)
    recursos = []
    for i in eventoRecursos:
        recursos.append(i.recursoid)
    context = {
        'object': recursos
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
    timedateRecursos = TimedateRecurso.objects.filter(recursoid_id=obj.id)
    for i in timedateRecursos:
        i.delete()
    for j in eventoRecursos:
        j.delete()
    obj.delete()
    innerObj.delete()
    messages.success(request, 'Recurso eliminado com sucesso')
    return redirect('Recurso:recursos')


def equipamentos(request):
    obj = Equipamento.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/old/equip_list.html', context)


def equipamento_create(request):
    form = EquipamentoForm(request.POST or None)
    form2 = RecursoForm(request.POST or None)
    if form.is_valid():
        empresaid = request.POST.get('empresaid')
        if empresaid != '':
            empresa = Empresa.objects.get(id=empresaid)
            fonte = 'Externa'
            recurso = Recurso(Nome=request.POST.get("Nome"), fonte=fonte, empresaid=empresa,
                              equipamentoid=form.instance)
        else:
            fonte = 'Interna'
            recurso = Recurso(Nome=request.POST.get("Nome"), fonte=fonte, equipamentoid=form.instance)
        form.save()
        recurso.save()
        messages.success(request, 'Equipamento criado com sucesso')
        return redirect('Recurso:recursos')
    else:
        error = form.errors
        if error.get("Nome"):
            messages.error(request, error.get("Nome"))
        elif error.get("Descrição"):
            messages.error(request, error.get("Descrição"))
    context = {
        'form': form,
        'form2': form2
    }
    return render(request, 'Recurso/equip_create.html', context)


def equipamento_update(request, my_id):
    obj = get_object_or_404(Equipamento, id=my_id)
    recurso = Recurso.objects.get(equipamentoid=my_id)
    form = EquipamentoForm(request.POST or None, instance=obj)
    form2 = RecursoForm(request.POST or None, instance=recurso)
    if form.is_valid():
        empresaid = request.POST.get('empresaid')
        if empresaid != '':
            fonte = 'Externa'
            empresa = Empresa.objects.get(id=empresaid)
            recurso.Nome = request.POST.get("Nome")
            recurso.empresaid = empresa
            recurso.fonte = fonte
        else:
            fonte = 'Interna'
            recurso.Nome = request.POST.get("Nome")
            recurso.fonte = fonte
            recurso.empresaid = None
        form.save()
        recurso.save()
        messages.success(request, 'Equipamento editado com sucesso')
        return redirect("Recurso:recursos")
    else:
        error = form.errors
        if error.get("Nome"):
            messages.error(request, error.get("Nome"))
        elif error.get("Descrição"):
            messages.error(request, error.get("Nome"))
    context = {
        'form': form,
        'form2': form2,
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
    return render(request, 'Recurso/old/espaco_list.html', context)


def espaco_create(request):
    form = EspacoForm(request.POST or None)
    form2 = RecursoForm(request.POST or None)
    if form.is_valid():
        empresaid = request.POST.get('empresaid')
        if empresaid != '':
            empresa = Empresa.objects.get(id=empresaid)
            fonte = 'Externa'
            recurso = Recurso(Nome=request.POST.get("Nome"), fonte=fonte, empresaid=empresa,
                              espacoid=form.instance)
        else:
            fonte = 'Interna'
            recurso = Recurso(Nome=request.POST.get("Nome"), fonte=fonte, espacoid=form.instance)
        form.save()
        recurso.save()
        messages.success(request, 'Espaço criado com sucesso')
        return redirect('Recurso:recursos')
    else:
        error = form.errors
        if error.get("__all__"):
            messages.error(request, error.get("__all__"))
        if error.get("capacidade"):
            messages.error(request, error.get("capacidade"))
    context = {
        'form': form,
        'form2': form2
    }
    return render(request, 'Recurso/espaco_create.html', context)


def espaco_update(request, my_id):
    obj = get_object_or_404(Espaco, id=my_id)
    recurso = Recurso.objects.get(espacoid=my_id)
    form = EspacoForm(request.POST or None, instance=obj)
    form2 = RecursoForm(request.POST or None, instance=recurso)
    if form.is_valid():
        empresaid = request.POST.get('empresaid')
        if empresaid != '':
            fonte = 'Externa'
            empresa = Empresa.objects.get(id=empresaid)
            recurso.Nome = request.POST.get("Nome")
            recurso.empresaid = empresa
            recurso.fonte = fonte
        else:
            fonte = 'Interna'
            recurso.Nome = request.POST.get("Nome")
            recurso.fonte = fonte
            recurso.empresaid = None
        form.save()
        recurso.save()
        messages.success(request, 'Espaço editado com sucesso')
        return redirect("Recurso:recursos")
    else:
        error = form.errors
        if error.get("__all__"):
            messages.error(request, error.get("__all__"))
    context = {
        'form': form,
        'form2': form2,
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
        empresaid = request.POST.get('empresaid')
        if empresaid != '':
            empresa = Empresa.objects.get(id=empresaid)
            fonte = 'Externa'
            recurso = Recurso(Nome=request.POST.get("Nome"), fonte=fonte, servicoid=form.instance, empresaid=empresa)
        else:
            fonte = 'Interna'
            recurso = Recurso(Nome=request.POST.get("Nome"), fonte=fonte, servicoid=form.instance)
            messages.success(request, 'Serviço criado com sucesso')
        form.save()
        recurso.save()
        return redirect('Recurso:recursos')
    else:
        error = form.errors
        if error.get("Nome"):
            messages.error(request, error.get("Nome"))
        elif error.get("Descrição"):
            messages.error(request, error.get("Nome"))

    context = {
        'form': form,
        'form2': form2
    }
    return render(request, 'Recurso/servico_create.html', context)


def servico_update(request, my_id):
    obj = get_object_or_404(Servico, id=my_id)
    recurso = Recurso.objects.get(servicoid=my_id)
    form = ServicoForm(request.POST or None, instance=obj)
    form2 = RecursoForm(request.POST or None, instance=recurso)
    empresaid = request.POST.get('empresaid')
    if form.is_valid():
        if empresaid != '':
            fonte = 'Externa'
            empresa = Empresa.objects.get(id=empresaid)
            recurso.Nome = request.POST.get("Nome")
            recurso.empresaid = empresa
            recurso.fonte = fonte
        else:
            fonte = 'Interna'
            recurso.Nome = request.POST.get("Nome")
            recurso.empresaid = None
            recurso.fonte = fonte
        form.save()
        recurso.save()
        messages.success(request, 'Serviço editado com sucesso')
        return redirect("Recurso:recursos")
    else:
        error = form.errors
        if error.get("Nome"):
            messages.error(request, error.get("Nome"))
        elif error.get("Descrição"):
            messages.error(request, error.get("Nome"))
    context = {
        'form': form,
        'form2': form2,
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
    return redirect('Recurso:recursos')


def empresas(request):
    obj = Empresa.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/old/empresa_list.html', context)


def empresa_create(request):
    form = EmpresaForm(request.POST or None)
    if form.is_valid():
        componente = Componente(Nome=request.POST.get("Nome"), empresaid=form.instance)
        form.save()
        componente.save()
        messages.success(request, 'Empresa criada com sucesso')
        return redirect('Recurso:componentes')
    else:
        error = form.errors
        if error.get("Nome"):
            messages.error(request, error.get("Nome"))
        if error.get("email"):
            messages.error(request, error.get("email"))
        if error.get("telefone"):
            messages.error(request, error.get("telefone"))
        if error.get("codigopostal"):
            messages.error(request, error.get("codigopostal"))
        if error.get("faturacao"):
            messages.error(request, error.get("faturacao"))
        if error.get("endereco"):
            messages.error(request, error.get("endereco"))
    context = {
        'form': form,
    }
    return render(request, 'Recurso/empresa_create.html', context)


def empresa_delete(request, my_id):
    obj = get_object_or_404(Empresa, id=my_id)
    obj.delete()
    messages.success(request, 'Empresa eliminada com sucesso')
    return redirect('Recurso:componentes')


def empresa_update(request, my_id):
    obj = get_object_or_404(Empresa, id=my_id)
    form = EmpresaForm(request.POST or None, instance=obj)
    if form.is_valid():
        componente = Componente.objects.get(empresaid=my_id)
        componente.Nome = request.POST.get("Nome")
        form.save()
        componente.save()
        messages.success(request, 'Empresa editada com sucesso')
        return redirect("Recurso:componentes")
    else:
        error = form.errors
        if error.get("Nome"):
            messages.error(request, error.get("Nome"))
        if error.get("email"):
            messages.error(request, error.get("email"))
        if error.get("telefone"):
            messages.error(request, error.get("telefone"))
        if error.get("codigopostal"):
            messages.error(request, error.get("codigopostal"))
        if error.get("faturacao"):
            messages.error(request, error.get("faturacao"))
        if error.get("endereco"):
            messages.error(request, error.get("endereco"))
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
    return render(request, 'Recurso/old/edificio_list.html', context)


def edificio_create(request):
    form = EdificioForm(request.POST or None)
    if form.is_valid():
        componente = Componente(Nome=request.POST.get("Nome"), edificioid=form.instance)
        form.save()
        componente.save()
        messages.success(request, 'Edifício criado com sucesso')
        return redirect('Recurso:componentes')
    else:
        error = form.errors
        if error.get("__all__"):
            messages.error(request, error.get("__all__"))
    context = {
        'form': form,
    }
    return render(request, 'Recurso/edificio_create.html', context)


def edificio_delete(request, my_id):
    obj = get_object_or_404(Edificio, id=my_id)
    obj.delete()
    messages.success(request, 'Edifício eliminado com sucesso')
    return redirect('Recurso:componentes')


def edificio_update(request, my_id):
    obj = get_object_or_404(Edificio, id=my_id)
    form = EdificioForm(request.POST or None, instance=obj)
    if form.is_valid():
        componente = Componente.objects.get(edificioid=my_id)
        componente.Nome = request.POST.get("Nome")
        form.save()
        componente.save()
        messages.success(request, 'Edifício editado com sucesso')
        return redirect("Recurso:componentes")
    else:
        error = form.errors
        if error.get("__all__"):
            messages.error(request, error.get("__all__"))
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
    return render(request, 'Recurso/old/unidade-organica_list.html', context)


def unidadeorganica_create(request):
    form = UnidadeOrganicaForm(request.POST or None)
    if form.is_valid():
        componente = Componente(Nome=request.POST.get("Nome"), unidade_organicaid=form.instance)
        form.save()
        componente.save()
        messages.success(request, 'Unidade Orgânica criada com sucesso')
        return redirect('Recurso:componentes')
    else:
        error = form.errors
        if error.get("__all__"):
            messages.error(request, error.get("__all__"))
    context = {
        'form': form,
    }
    return render(request, 'Recurso/unidade-organica_create.html', context)


def unidadeorganica_delete(request, my_id):
    obj = get_object_or_404(Unidadeorganica, id=my_id)
    obj.delete()
    messages.success(request, 'Unidade Orgânica eliminada com sucesso')
    return redirect('Recurso:componentes')


def unidadeorganica_update(request, my_id):
    obj = get_object_or_404(Unidadeorganica, id=my_id)
    form = UnidadeOrganicaForm(request.POST or None, instance=obj)
    print(form.fields)
    if form.is_valid():
        componente = Componente.objects.get(unidadeorganicaid=my_id)
        componente.Nome = request.POST.get("Nome")
        form.save()
        componente.save()
        messages.success(request, 'Unidade orgânica editada com sucesso')
        return redirect("Recurso:componentes")
    else:
        error = form.errors
        if error.get("__all__"):
            messages.error(request, error.get("__all__"))
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
    return render(request, 'Recurso/old/universidade_list.html', context)


def universidade_create(request):
    form = UniversidadeForm(request.POST or None)
    if form.is_valid():
        componente = Componente(Nome=request.POST.get("Nome"), universidadeid=form.instance)
        form.save()
        componente.save()
        messages.success(request, 'Universidade criada com sucesso')
        return redirect('Recurso:componentes')
    else:
        error = form.errors
        if error.get("__all__"):
            messages.error(request, error.get("__all__"))
    context = {
        'form': form,
    }
    return render(request, 'Recurso/universidade_create.html', context)


def universidade_update(request, my_id):
    obj = get_object_or_404(Universidade, id=my_id)
    form = UniversidadeForm(request.POST or None, instance=obj)
    if form.is_valid():
        componente = Componente.objects.get(universidadeid=my_id)
        componente.Nome = request.POST.get("Nome")
        form.save()
        componente.save()
        messages.success(request, 'Universidade editada com sucesso')
        return redirect("Recurso:componentes")
    else:
        error = form.errors
        if error.get("__all__"):
            messages.error(request, error.get("__all__"))
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
    messages.success(request, 'Universidade eliminada com sucesso')
    return redirect('Recurso:componentes')


def campis(request):
    obj = Campus.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'Recurso/old/campus_list.html', context)


def campus_create(request):
    form = CampusForm(request.POST or None)
    if form.is_valid():
        componente = Componente(Nome=request.POST.get("Nome"), campusid=form.instance)
        form.save()
        componente.save()
        messages.success(request, 'Campus criado com sucesso')
        return redirect('Recurso:componentes')
    else:
        error = form.errors
        if error.get("__all__"):
            messages.error(request, error.get("__all__"))
    context = {
        'form': form,
    }
    return render(request, 'Recurso/campus_create.html', context)


def campus_update(request, my_id):
    obj = get_object_or_404(Campus, id=my_id)
    form = CampusForm(request.POST or None, instance=obj)
    if form.is_valid():
        componente = Componente.objects.get(campusid=my_id)
        componente.Nome = request.POST.get("Nome")
        form.save()
        componente.save()
        messages.success(request, 'Campus editado com sucesso')
        return redirect("Recurso:componentes")
    else:
        error = form.errors
        if error.get("__all__"):
            messages.error(request, error.get("__all__"))
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
    messages.success(request, 'Campus eliminado com sucesso')
    return redirect('Recurso:componentes')
