from django.shortcuts import redirect, render
from Neglected.models import Timedate
from .models import Evento, Logistica, Tipoevento
from Recurso.models import Tipodeequipamento, Tipoespaco, Tiposervico
from GestorTemplates.models import Formulario, CampoFormulario, Campo, Resposta
from Utilizadores.models import User
from django.db.models import Q
from django.contrib import messages
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers


def ajax_finalizar_logistica(request):
    if request.method == "POST":
        msg = request.POST["myData"]
        event_id = request.POST["id"]
        evento = Evento.objects.get(id=event_id)
        campo = Campo.objects.get(conteudo="Estado do evento")
        resposta_estado = Resposta.objects.filter(campoid=campo)
        reposta = None
        logistica = Logistica.objects.get(eventoid=evento)
        espacos = Tipoespaco.objects.filter(logisticaid=logistica)
        equipamentos = Tipodeequipamento.objects.filter(logisticaid=logistica)
        servicos = Tiposervico.objects.filter(logisticaid=logistica)


        for resp in resposta_estado:
            if resp.eventoid == evento:
                resposta = resp
                if msg == "true":
                    evento.estado = "Pendente"
                    evento.save()
                    resposta.conteudo = "Pendente"
                    resposta.save()

                    # Delete all logisticas
                    for item in espacos:
                        item.delete()
                    for item in equipamentos:
                        item.delete()
                    for item in servicos:
                        item.delete()

                    messages.success(request, 'Logistica recusada, o evento voltou para o estado inicial')

                else:
                    evento.estado = "Logistica Validada"
                    evento.save()
                    resposta.conteudo = "Logistica Validada"
                    resposta.save()
                    messages.success(request, 'Logistica finalizada com sucesso.')

        
        data = {
            "msg": "200"
        }
        return JsonResponse(data)

# Filter by type
def ajax_filter_type(request):
    if request.method == "POST":
        msg = request.POST["myData"]
        tipo = Tipoevento.objects.filter(nome=msg)
        if msg == "reset":
            events = Evento.objects.filter(estado='Aceite')
        else:
            events = Evento.objects.filter(estado='Aceite', tipoeventoid=tipo[0])
        eventos = []
        for e in events:
            hora = Timedate.objects.get(id=e.horario.id)
            eventos.append({
                "nome": e.nome,
                "hora": f"{e.horario.horainicial}-{e.horario.horafinal}",
                "data": f"{e.horario.datainicial.day}/{e.horario.datainicial.month}/{e.horario.datainicial.year} - {e.horario.datafinal.day}/{e.horario.datafinal.month}/{e.horario.datafinal.year}",
            })
        data = {
            "msg": msg,
            "eventos": eventos
        }
        return JsonResponse(data)
    if request.method == "GET":
        eventos = Evento.objects.filter(estado='Aceite')
        dat = serializers.serialize('json', eventos)
        data = {
            "eventos": dat
        }
        return JsonResponse(data)


# Filter by state
def ajax_filter_state(request):
    if request.method == "POST":
        # Get current user
        user = get_user(request)

        # Get user type
        id_gcp = user[0].gcpid
        id_prop_i = user[0].proponente_internoid
        id_ext_i = user[0].proponente_externoid

        msg = request.POST["myData"]
        if msg == "reset":
            events = Evento.objects.filter(proponente_externoid=id_ext_i, proponente_internoid=id_prop_i)
            eventos = []
        else:
            events = Evento.objects.filter(estado=msg, proponente_externoid=id_ext_i, proponente_internoid=id_prop_i)
            eventos = []

        for e in events:
   
            hora = Timedate.objects.get(id=e.horario.id)
            eventos.append({
                "nome": e.nome,
                "estado": e.estado,
                "data": f"{e.horario.datainicial.day}/{e.horario.datainicial.month}/{e.horario.datainicial.year} {e.horario.horainicial} - {e.horario.datafinal.day}/{e.horario.datafinal.month}/{e.horario.datafinal.year} {e.horario.horafinal}",
                
            })
        data = {
            "msg": msg,
            "eventos": eventos
        }
        return JsonResponse(data)




# Homepage.
def home_view(request):
    return render(request, 'inicio.html')


# Show all the events that has the final validation.
def eventos(request):
    events = Evento.objects.filter(estado='Aceite')
    logistica = Logistica.objects.all()
    tipos = Tipoevento.objects.all()

    context = {
        'eventos': events,
        'logistica': logistica,
        'tipos': tipos
    }

    return render(request, 'Evento/eventos.html', context)


# Show all the events that as been created so GCP users can manage it.
# Only GCP user will have access.
def eventos_gerir(request):

    events = Evento.objects.all()
    logistica = Logistica.objects.all()

    context = {
        'eventos': events,
        'logistica': logistica,
    }
    
    return render(request, 'Evento/eventos_gerir.html', context)

def validar_evento(request, event_id):
    evento = Evento.objects.get(id=event_id)
    evento.estado = "Validado"
    evento.save()

    messages.success(request, 'Evento validado com sucesso.')
    return redirect("Evento:eventos-gerir")

def recusar_evento(request, event_id):
    evento = Evento.objects.get(id=event_id)
    evento.estado = "Recusado"
    evento.save()

    messages.success(request, 'O evento foi recusado.')
    return redirect("Evento:eventos-gerir")


# Show events created by the current user.
def meus_eventos(request):
    # Get current user
    user = get_user(request)

    # Get user type
    id_gcp = user[0].gcpid
    id_prop_i = user[0].proponente_internoid
    id_ext_i = user[0].proponente_externoid

    # Get events created by current user
    # TODO: change filter.
    events = Evento.objects.filter(proponente_externoid=id_ext_i, proponente_internoid=id_prop_i)  # temporary
    logistica = Logistica.objects.all()

    context = {
        'eventos': events,
        'logistica': logistica
    }
    return render(request, 'Evento/meus_eventos.html', context)


# Give the user the option to choose which type of logistic the user wants to create to the given event.
def create_logistic(request, event_id):
    evento = Evento.objects.get(id=event_id)
    logistica = Logistica.objects.filter(eventoid=evento)
    if not logistica:
        new_logista = Logistica(nome=f'logistica-{evento.id}', eventoid=evento)
        new_logista.save()

    context = {
        'evento': evento,
    }
    return render(request, 'Evento/criar_logistica.html', context)


# Equipament Logistic
def equip_logistic(request, event_id):
    equip = Tipodeequipamento()
    return render_logistic_form_by_type(request, event_id, equip, 1)


# Espaco Logistic
def espaco_logistic(request, event_id):
    espaco = Tipoespaco()
    return render_logistic_form_by_type(request, event_id, espaco, 2)


# Servico Logistic
def servico_logistic(request, event_id):
    servico = Tiposervico()
    return render_logistic_form_by_type(request, event_id, servico, 3)


# Submit logistic to the GCP
def submit_logistic(request, event_id):
    evento = Evento.objects.get(id=event_id)
    evento.estado = 'Logistica Pendente'
    evento.save()
    messages.success(request, 'Logistica submetida com sucesso. Favor aguardar a resposta do GCP')
    return redirect('Evento:meus-eventos')

# Submit event to GCP
def submeter_event(request, event_id):
    evento = Evento.objects.get(id=event_id)
    evento.estado = 'Submetido'
    evento.save()
    messages.success(request, 'Evento submetido com sucesso. Favor aguardar a resposta final do GCP')
    return redirect('Evento:meus-eventos')

# Aceitar Evento
def aceitar_event(request, event_id):
    evento = Evento.objects.get(id=event_id)
    evento.estado = 'Aceite'
    evento.save()
    messages.success(request, 'Evento aceite com sucesso.')
    return redirect('Evento:eventos-gerir')


# Return page to manage the given event
def gerir(request, event_id):
    evento = Evento.objects.get(id=event_id)

    formulario = Formulario.objects.filter(tipoeventoid=evento.tipoeventoid, tipoformularioid=3)
    perguntas = CampoFormulario.objects.filter(formularioid=formulario[0]).exclude(Q(campoid_id=22) | Q(campoid_id=23)).order_by('campoid')
    respostas = Resposta.objects.filter(eventoid=evento)

    context = {
        'evento': Evento.objects.get(id=event_id),
        'id': event_id,
        'perguntas': perguntas,
        'respostas': respostas
    }
    return render(request, 'Evento/gerir.html', context)

# Delete Event
def delete_event(request, event_id):
    evento = Evento.objects.get(id=event_id)
    respostas = Resposta.objects.filter(eventoid=evento)
    for resposta in respostas:
        resposta.delete()
    evento.delete()
    messages.success(request, 'Evento removido com sucesso')
    return redirect('Evento:meus-eventos')



# Edit Event
def edit_event(request, event_id):
    evento = Evento.objects.get(id=event_id)
    formulario = Formulario.objects.filter(tipoeventoid=evento.tipoeventoid, tipoformularioid=3)
    perguntas = CampoFormulario.objects.filter(formularioid=formulario[0]).exclude(Q(campoid_id=22) | Q(campoid_id=23)).order_by('campoid')
    respostas = Resposta.objects.filter(eventoid=evento)
    for pergunta in perguntas:
        if pergunta.campoid.tipocampoid.nome == 'Escolha Múltipla' or \
                pergunta.campoid.tipocampoid.nome == 'Dropdown':
            pergunta.campoid.respostas = pergunta.campoid.respostapossivelid.nome.split(",")

    horario = evento.horario
    if request.method == 'POST':
        for pergunta in perguntas:
            id = pergunta.campoid.id
            if id == 10:
                nome = request.POST.get(f'{id}')
                evento.nome = nome
                resposta = Resposta.objects.get(eventoid=evento, campoid=pergunta.campoid)
                resposta.conteudo = nome
                resposta.save()
            elif id == 11:
                desc = request.POST.get(f'{id}')
                evento.descricaogeral = desc
                resposta = Resposta.objects.get(eventoid=evento, campoid=pergunta.campoid)
                resposta.conteudo = desc
                resposta.save()
            elif id == 12:
                num_p = request.POST.get(f'{id}')
                evento.maxparticipantes = num_p
                resposta = Resposta.objects.get(eventoid=evento, campoid=pergunta.campoid)
                resposta.conteudo = num_p
                resposta.save()
            elif id == 31:
                val = request.POST.get(f'{id}')
                if val == 'Sim':
                    val = 1
                else:
                    val = 0
                evento.val_inscritos = val
                resposta = Resposta.objects.get(eventoid=evento, campoid=pergunta.campoid)
                resposta.conteudo = val
                resposta.save()
            elif id == 14:
                data_i = request.POST.get(f'{id}')
                horario.datainicial = data_i
                resposta = Resposta.objects.get(eventoid=evento, campoid=pergunta.campoid)
                resposta.conteudo = data_i
                resposta.save()
            elif id == 15:
                data_f = request.POST.get(f'{id}')
                horario.datafinal = data_f
                resposta = Resposta.objects.get(eventoid=evento, campoid=pergunta.campoid)
                resposta.conteudo = data_f
                resposta.save()
            elif id == 16:
                hora_i = request.POST.get(f'{id}')
                horario.horainicial = hora_i
                resposta = Resposta.objects.get(eventoid=evento, campoid=pergunta.campoid)
                resposta.conteudo = hora_i
                resposta.save()
            elif id == 17:
                hora_f = request.POST.get(f'{id}')
                horario.horafinal = hora_f
                resposta = Resposta.objects.get(eventoid=evento, campoid=pergunta.campoid)
                resposta.conteudo = hora_f
                resposta.save()
            
        horario.save()
        evento.estado = 'Pendente'
        evento.save()
        messages.success(request, 'Evento alterado com sucesso')

        return redirect('Evento:meus-eventos')

    context = {
        'evento': evento,
        'campos': perguntas,
        'respostas': respostas
    }
    return render(request, 'Evento/edit_evento.html', context)


# Create an event after the form is submitted
def create_event(request, type_id, type_evento):
    user = get_user(request)
    tipo = get_user_type(request)
    id_gcp = user[0].gcpid
    id_prop_i = user[0].proponente_internoid
    id_ext_i = user[0].proponente_externoid

    formulario = Formulario.objects.filter(id=type_id)
    perguntas = CampoFormulario.objects.filter(formularioid=formulario[0]).exclude(Q(campoid_id=22) | Q(campoid_id=23)).order_by('campoid')

    for pergunta in perguntas:
        if pergunta.campoid.tipocampoid.nome == 'Escolha Múltipla' or \
                pergunta.campoid.tipocampoid.nome == 'Dropdown':
            pergunta.campoid.respostas = pergunta.campoid.respostapossivelid.nome.split(",")

    evento = Evento()
    horario = Timedate()
    respostas = []

    if request.method == 'POST':
        for pergunta in perguntas:
            id = pergunta.campoid.id
            if id == 10:
                nome = request.POST.get(f'{id}')
                evento.nome = nome
            elif id == 11:
                desc = request.POST.get(f'{id}')
                evento.descricaogeral = desc
            elif id == 12:
                num_p = request.POST.get(f'{id}')
                evento.maxparticipantes = num_p
            elif id == 31:
                val = request.POST.get(f'{id}')
                if val == 'Sim':
                    val = 1
                else:
                    val = 0
                evento.val_inscritos = val
            elif id == 14:
                data_i = request.POST.get(f'{id}')
                horario.datainicial = data_i
            elif id == 15:
                data_f = request.POST.get(f'{id}')
                horario.datafinal = data_f
            elif id == 16:
                hora_i = request.POST.get(f'{id}')
                horario.horainicial = hora_i
            elif id == 17:
                hora_f = request.POST.get(f'{id}')
                horario.horafinal = hora_f
            resposta = Resposta(conteudo=request.POST.get(f'{id}'), campoid=pergunta.campoid, eventoid=evento)
            respostas.append(resposta)

        horario.save()
        evento.inscritos = 0
        evento.estado = "Pendente"
        evento.proponente_internoid = id_prop_i
        evento.proponente_externoid = id_ext_i
        evento.horario = horario
        tipo_evento = Tipoevento.objects.get(id=type_evento)
        evento.tipoeventoid = tipo_evento

        evento.save()
        messages.success(request, 'Evento criado com sucesso')

        for resp in respostas:
            resp.save()

        resposta_estado = Resposta(conteudo='Pendente', campoid_id=32, eventoid=evento)
        resposta_estado.save()
        resposta_inscritos = Resposta(conteudo=0, campoid_id=23, eventoid=evento)
        resposta_inscritos.save()
        # Redirect to eventos page
        return redirect('Evento:meus-eventos')


    context = {
        'campos': perguntas
    }
    return render(request, 'Evento/criar_evento.html', context)


def select_type(request):
    tipos = Tipoevento.objects.all()

    if request.method == 'POST':
        tipo = request.POST['radio']
        return redirect('Evento:select_form', tipo)

    context = {
        'tipos': tipos
    }
    return render(request, 'Evento/selecionar_tipo.html', context)

def select_form(request, type_id):
    formularios = Formulario.objects.filter(tipoeventoid=type_id, tipoformularioid=3)

    if request.method == 'POST':
        tipo = request.POST['radio']
        return redirect('Evento:create-event', tipo, type_id)

    context = {
        'tipos': formularios
    }
    return render(request, 'Evento/selecionar_form.html', context)


# Delete logistica
def delete_logistica(request, event_id):
    evento = Evento.objects.get(id=event_id)
    logistica = Logistica.objects.get(eventoid=evento)
    tipoespaco = Tipoespaco.objects.filter(logisticaid=logistica)
    tipoequipamento = Tipodeequipamento.objects.filter(logisticaid=logistica)
    tiposervico = Tiposervico.objects.filter(logisticaid=logistica)

    # Delete all dependencies 
    for item in tipoespaco:
        item.delete()

    for item in tipoequipamento:
            item.delete()
        
    for item in tiposervico:
            item.delete()



    logistica.delete()
    evento.estado = "Validado"
    evento.save()
    messages.success(request, 'Logistica removida com sucesso')
    return redirect("Evento:meus-eventos")

# Edit logistica
def edit_logistica(request, event_id):
    evento = Evento.objects.get(id=event_id)
    logistica = Logistica.objects.get(eventoid=evento)
    tipoespaco = Tipoespaco.objects.filter(logisticaid=logistica)
    tipoequipamento = Tipodeequipamento.objects.filter(logisticaid=logistica)
    tiposervico = Tiposervico.objects.filter(logisticaid=logistica)

    context = {
        "evento": evento,
        "logistica": logistica,
        "espacos": tipoespaco,
        "equipamentos": tipoequipamento,
        "servicos": tiposervico
    }

    return render(request, 'Evento/edit_logistica.html', context)

# Edit espaco logistica
def edit_espaco(request, event_id, espaco_id, tipo):
    evento = Evento.objects.get(id=event_id)
    logistica = Logistica.objects.get(eventoid=evento)


    if tipo == 'espaco':
        obj = Tipoespaco.objects.get(logisticaid=logistica, id=espaco_id)
    elif tipo == 'equipamento':
        obj = Tipodeequipamento.objects.get(logisticaid=logistica, id=espaco_id)
    elif tipo == 'servico': 
        obj = Tiposervico.objects.get(logisticaid=logistica, id=espaco_id)


    formulario = Formulario.objects.filter(tipoformularioid=4)
    perguntas = CampoFormulario.objects.filter(formularioid=formulario[0]).order_by('campoid')

    horario = obj.horariorequisicao

    hora_i = horario.horainicial
    hora_f = horario.horafinal
    data_i = horario.datainicial
    data_f = horario.datafinal

    # Get multiple choices and bind to the pergunta obj
    for pergunta in perguntas:
        if pergunta.campoid.tipocampoid.nome == 'Escolha Múltipla' or \
                pergunta.campoid.tipocampoid.nome == 'Dropdown':
            pergunta.campoid.respostas = pergunta.campoid.respostapossivelid.nome.split(",")


    if request.method == 'POST':
        obj.nome = request.POST.get("desc")
        obj.quantidade = request.POST.get("quantidade")
        dataI = request.POST.get("data_i")
        dataF = request.POST.get("data_f")
        horaI = request.POST.get("hora_i")
        horaF = request.POST.get("hora_f")
        novaHora = Timedate()
        novaHora.datainicial = dataI
        novaHora.datafinal = dataF 
        novaHora.horainicial = horaI 
        novaHora.horafinal = horaF 
        novaHora.save()
        obj.horariorequisicao = novaHora
        obj.save()

        messages.success(request, 'Pedido alterado com sucesso')
        
        return redirect("Evento:edit-logistica", event_id)

    

    context = {
        "evento": evento,
        "logistica": logistica,
        "obj": obj, 
        "campos": perguntas,
        "hora_i": hora_i,
        "hora_f": hora_f,
        "data_i": data_i,
        "data_f": data_f,
        "tipo": tipo
    }

    return render(request, 'Evento/edit_espaco.html', context)

# Edit servico logistica
def edit_servico(request, event_id):
    evento = Evento.objects.get(id=event_id)
    logistica = Logistica.objects.get(eventoid=evento)
    tiposervico = Tiposervico.objects.filter(logisticaid=logistica)

    context = {
        "evento": evento,
        "logistica": logistica,
        "espacos": tipoespaco, 
    }

    return render(request, 'Evento/edit_servico.html', context)

# Edit equipamento logistica
def edit_equipamento(request, event_id):
    evento = Evento.objects.get(id=event_id)
    logistica = Logistica.objects.get(eventoid=evento)
    tipoequipamento = Tipodeequipamento.objects.filter(logisticaid=logistica)

    context = {
        "evento": evento,
        "logistica": logistica,
        "espacos": tipoespaco, 
    }

    return render(request, 'Evento/edit_equipamento.html', context)


# View Logisticas
def view_logisticas(request, event_id):
    evento = Evento.objects.get(id=event_id)
    logistica = Logistica.objects.get(eventoid=evento)
    logistica_equipamento = Tipodeequipamento.objects.filter(logisticaid=logistica)
    logistica_servico = Tiposervico.objects.filter(logisticaid=logistica)
    logistica_espaco = Tipoespaco.objects.filter(logisticaid=logistica)

    context = {
        'equipamentos': logistica_equipamento,
        'servicos': logistica_servico,
        'espacos': logistica_espaco,
        'evento': evento,
    }
    return render(request, 'Evento/view_logistica.html', context)


# View a specific event
def view_event(request, event_id):
    evento = Evento.objects.get(id=event_id)

    horario = Timedate.objects.get(id=evento.horario.id)

    context = {
        'evento': evento,
        'data_i': horario.datainicial,
        'data_f': horario.datafinal,
        'hora_i': horario.horainicial,
        'hora_f': horario.horafinal,
    }
    return render(request, 'Evento/view_evento.html', context)


# View a specific event
def view_my_event(request, event_id):
    evento = Evento.objects.get(id=event_id)

    formulario = Formulario.objects.filter(tipoeventoid=evento.tipoeventoid, tipoformularioid=3)
    perguntas = CampoFormulario.objects.filter(formularioid=formulario[0]).exclude(Q(campoid_id=22) | Q(campoid_id=23)).order_by('campoid')
    respostas = Resposta.objects.filter(eventoid=evento)

    context = {
        'evento': Evento.objects.get(id=event_id),
        'id': event_id,
        'perguntas': perguntas,
        'respostas': respostas
    }
    return render(request, 'Evento/view_my_event.html', context)





# HELPER FUNCTIONS
def get_user_type(request):
    user_django = request.user
    user = User.objects.filter(email=user_django.email)
    if user[0].gcpid is not None:
        tipo = 'gcp'
    elif user[0].proponente_internoid is not None:
        tipo = 'interno'
    elif user[0].proponente_externoidid is not None:
        tipo = 'externo'
    elif user[0].servicostecnicosid is not None:
        tipo = 'servicos'
    else:
        tipo = None
    return tipo


def get_user(request):
    user_django = request.user
    user = User.objects.filter(email=user_django.email)
    return user


def render_logistic_form_by_type(request, event_id, obj, type_logistic):
    # Event.
    evento = Evento.objects.get(id=event_id)

    # Logistic
    logistic = Logistica.objects.filter(eventoid=evento)

    # Retrieve logistic form for the given event.
    formulario = Formulario.objects.filter(tipoformularioid=4)
    perguntas = CampoFormulario.objects.filter(formularioid=formulario[0]).order_by('campoid')

    # Get multiple choices and bind to the pergunta obj
    for pergunta in perguntas:
        if pergunta.campoid.tipocampoid.nome == 'Escolha Múltipla' or \
                pergunta.campoid.tipocampoid.nome == 'Dropdown':
            pergunta.campoid.respostas = pergunta.campoid.respostapossivelid.nome.split(",")

    horario = Timedate()

    if request.method == 'POST':
        get_data_from_form(request, obj, perguntas, horario, logistic[0], evento)

        # Redirect to eventos page
        messages.success(request, 'Pedido adicionado com sucesso, podera adicionar mais ou se finalizado, favor submeter a logistica')
        return redirect('Evento:meus-eventos')
        
    else:
        context = {
            'evento': evento,
            'campos': perguntas
        }
        if type_logistic == 1:
            return render(request, 'Evento/equipamento_logistica.html', context)
        elif type_logistic == 2:
            return render(request, 'Evento/espaco_logistica.html', context)
        elif type_logistic == 3:
            return render(request, 'Evento/servico_logistica.html', context)
        else:
            return render(request, 'Evento/eventos.html', context)


def get_data_from_form(request, tipo, perguntas, horario, logistica, evento):
    for pergunta in perguntas:
        id_p = pergunta.campoid.id
        if id_p == 11:
            desc = request.POST.get(f'{id_p}')
            tipo.nome = desc
        elif id_p == 14:
            data_i = request.POST.get(f'{id_p}')
            horario.datainicial = data_i
        elif id_p == 15:
            data_f = request.POST.get(f'{id_p}')
            horario.datafinal = data_f
        elif id_p == 16:
            hora_i = request.POST.get(f'{id_p}')
            horario.horainicial = hora_i
        elif id_p == 17:
            hora_f = request.POST.get(f'{id_p}')
            horario.horafinal = hora_f

    horario.save()
    tipo.horariorequisicao = horario
    tipo.quantidade = 1
    tipo.logisticaid = logistica
    tipo.save()
