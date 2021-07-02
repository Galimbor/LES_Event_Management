from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from GestorTemplates.models import Tipoformulario, Formulario, CampoFormulario, Campo, Resposta
from Utilizadores.models import User
from .forms import InscricaoForm, InscricaoUpdateForm, InscricaoCheckinUpdateForm
from Evento.models import Evento
from .models import Inscricao
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from eventoFormulario.models import EventoFormulario
from datetime import date, datetime

# -------- Views associadas ao perfl de PARTICIPANTES -----------------------------------------------------

# TODO : fazer uma outra versão para utilizadores autenticados
def CriarInscricao(request, eventoid):
    evento = Evento.objects.get(id=eventoid)

    if evento.inscritos == evento.maxparticipantes:
        messages.error(request, f'O número máximo de inscritos foi atingido.')

        return redirect('Evento:eventos')

    if evento.visibilidade == "Privado" and  not request.user.is_authenticated :
        messages.error(request, f"Precisa de estar logged in para se inscrever em eventos privados.")

    if request.user.is_authenticated :

        if Inscricao.objects.filter(eventoid=eventoid,email=request.user.email).exists():
            messages.error(request, f'Já se encontra inscrito neste evento!')
            return redirect('Evento:eventos')

        formularioEvento = EventoFormulario.objects.filter(eventoid=evento.id,
                                                           formularioid__tipoFormulario__categoria=1)

        formularioInscricao = formularioEvento[0].formularioid

        perguntas = CampoFormulario.objects.filter(formularioid=formularioInscricao.id,
                                                   campoid__campo_relacionado=None).exclude(campoid_id=28).exclude(
            campoid_id=27).exclude(campoid_id=1).exclude(campoid_id=2).exclude(campoid_id=3)

        for pergunta in perguntas:
            if (pergunta.campoid.tipocampoid.nome == "Escolha Múltipla" or
                    pergunta.campoid.tipocampoid.nome == 'Dropdown'):
                pergunta.campoid.respostas = Campo.objects.filter(campo_relacionado=pergunta.campoid)

    else :
        formularioEvento = EventoFormulario.objects.filter(eventoid=evento.id,
                                                           formularioid__tipoFormulario__categoria=1)

        formularioInscricao = formularioEvento[0].formularioid

        perguntas = CampoFormulario.objects.filter(formularioid=formularioInscricao.id,
                                                   campoid__campo_relacionado=None).exclude(campoid_id=28).exclude(
            campoid_id=27)

        for pergunta in perguntas:
            if (pergunta.campoid.tipocampoid.nome == "Escolha Múltipla" or
                    pergunta.campoid.tipocampoid.nome == 'Dropdown'):
                pergunta.campoid.respostas = Campo.objects.filter(campo_relacionado=pergunta.campoid)

    if request.method == 'POST':
        temp_email =  request.POST.get("3")
        if Inscricao.objects.filter(eventoid=eventoid,email=temp_email).exists():
            messages.error(request, f'Já existe uma inscrição com este email!')
            context = {
                'form': perguntas,
                'evento': evento,
            }
            return render(request, 'inscricao/participantes/inscricao_create.html', context)
        # TODO : Aqui deve acontecer alguma validação dos campos submetidos

        if request.user.is_authenticated:
            num_inscricao = evento.inscritos + 1

            evento.inscritos = evento.inscritos + 1
            evento.save()

            respostas = []

            inscricao = Inscricao(eventoid=evento)
            user_django = request.user
            user = User.objects.filter(email=user_django.email)[0]
            today = date.today()
            inscricao.idade = today.year - user.datanascimento.year
            inscricao.nome = f"{user.first_name} {user.last_name}"
            inscricao.email = user.email
            for pergunta in perguntas:
                perguntaid = pergunta.campoid.id
                # print(perguntaid)
                resposta = request.POST.get(f"{perguntaid}")
                if perguntaid == 4:  # NUMERO TELEMOVEL
                    inscricao.telemovel = resposta
                elif perguntaid == 5:  # PROFISSAO
                    inscricao.profissao = resposta
                respostas.append(Resposta(conteudo=resposta, inscricaoid=inscricao, campoid=pergunta.campoid))

            if evento.val_inscritos:
                estado = "Pendente"
            else:
                estado = "Confirmado"



            inscricao.eventoid = evento
            inscricao.userid = user

            inscricao.estado = estado
            respostas.append(Resposta(conteudo=estado, inscricaoid=inscricao, campoid=Campo.objects.get(id=27)))

            inscricao.num_inscricao = num_inscricao

            inscricao.checkin = 0
            respostas.append(Resposta(conteudo=0, inscricaoid=inscricao, campoid=Campo.objects.get(id=28)))

            inscricao.save()

            for resposta in respostas:
                resposta.save()

            messages.success(request, f'Concluiu a sua inscrição com sucesso!')

            return redirect('Evento:eventos')

        else:
            num_inscricao = evento.inscritos + 1

            evento.inscritos = evento.inscritos + 1
            evento.save()

            respostas = []

            inscricao = Inscricao(eventoid=evento)
            for pergunta in perguntas:
                perguntaid = pergunta.campoid.id
                # print(perguntaid)
                resposta = request.POST.get(f"{perguntaid}")
                # print(resposta)
                if perguntaid == 1:  # NOME
                    inscricao.nome = resposta
                elif perguntaid == 2:  # IDADE
                    print("im here")
                    inscricao.idade = resposta
                elif perguntaid == 3:  # EMAIL
                    inscricao.email = resposta
                elif perguntaid == 4:  # NUMERO TELEMOVEL
                    inscricao.telemovel = resposta
                elif perguntaid == 5:  # PROFISSAO
                    inscricao.profissao = resposta
                respostas.append(Resposta(conteudo=resposta, inscricaoid=inscricao, campoid=pergunta.campoid))

            if evento.val_inscritos:
                estado = "Pendente"
            else:
                estado = "Confirmado"


            userid = None

            inscricao.eventoid = evento
            inscricao.userid = userid

            inscricao.estado = estado
            respostas.append(Resposta(conteudo=estado, inscricaoid=inscricao, campoid=Campo.objects.get(id=27)))

            inscricao.num_inscricao = num_inscricao

            inscricao.checkin = 0
            respostas.append(Resposta(conteudo=0, inscricaoid=inscricao, campoid=Campo.objects.get(id=28)))

            inscricao.save()

            for resposta in respostas:
                resposta.save()

            messages.success(request, f'Concluiu a sua inscrição com sucesso!')

            return redirect('Evento:eventos')

    if len(perguntas) == 0:
        messages.success(request, f'Concluiu a sua inscrição com sucesso!')


        return redirect('Evento:eventos')

    context = {
        'form': perguntas,
        'evento' : evento,
    }
    return render(request, 'inscricao/participantes/inscricao_create.html', context)


# TODO: melhorar a consulta com filtros e barra de procura
class PartConsultarInscricoes(ListView):
    # We don't have users yet.
    # if not request.user.is_authenticated:
    #         messages.error(request, f'Por favor, faça login primeiro.')
    #         return redirect('Inscricao:list_inscricao')

    template_name = 'inscricao/participantes/list_inscricao2.html'

    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_django = self.request.user
            user = User.objects.filter(email=user_django.email)
            realuser = user[0]
            # return Inscricao.objects.filter(userid=realuser.id)
            queryset = Inscricao.objects.filter(userid=realuser.id)
            for inscricao in queryset:
                today = datetime.today()
                eventoDataFinal = inscricao.eventoid.horario.datafinal
                eventoHoraFinal = inscricao.eventoid.horario.horafinal
                eventFinalDate = datetime.combine(eventoDataFinal,eventoHoraFinal)
                if eventFinalDate < today and EventoFormulario.objects.filter(eventoid=inscricao.eventoid, formularioid__tipoFormulario__categoria=2).exists() :
                    inscricao.hasFeedback = True
            return queryset
        else:
            return None

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated :
            messages.error(request, f'Por favor, faça login primeiro.')
            return redirect('Evento:eventos')
        return super(PartConsultarInscricoes, self).get(request,*args,**kwargs)

    # Show the inscricoes of the users
    # def get_queryset(self):
        # return Inscricao.objects.filter(userid=self.request.user)


# TODO : apenas para utilizadores logged in
def PartInscricaoCancelar(request, inscricaoid):
    # We don't have users yet.
    # if not request.user.is_authenticated:
    #         messages.error(request, f'Por favor, faça login primeiro.')
    #         return redirect('Inscricao:inscricao')

    inscricao = Inscricao.objects.get(id=inscricaoid)

    respostas = Resposta.objects.filter(inscricaoid=inscricao)

    for resposta in respostas:
        resposta.delete()

    evento = inscricao.eventoid

    evento.inscritos -= 1

    evento.save()

    inscricao.delete()

    # print("what")
    messages.success(request, f'Eliminou a sua inscrição com sucesso!')

    return redirect('Inscricao:part_list_inscricao')
    # return render(request, 'inscricao/participantes/list_inscricao.html')


#TODO - ISTO VAI SER UMA FUNCIONALIDADE PARA OS PROPONENTES E DEVE ESTAR DIVIIDA
def PartInscricaoCheckin(request, id):
    inscricao = Inscricao.objects.get(id=id)

    respostas = Resposta.objects.filter(inscricaoid=inscricao)

    perguntas = []

    checkin = None

    for resposta in respostas:
        perguntas.append(resposta.campoid)
        if resposta.campoid.id == 28:
            checkin = resposta
            checkin.respostas = resposta.campoid.respostapossivelid.nome.split(",")

    QAA = zip(perguntas, respostas)

    if request.method == "POST":

        inscricao.checkin = request.POST.get(f"{28}") == 'Vou' if 1 else 0

        respostadb = Resposta.objects.get(inscricaoid=inscricao, campoid_id=28)

        if request.POST.get(f"{28}") == 'Vou':
            respostadb.conteudo = "1"
        else:
            respostadb.conteudo = "0"

        respostadb.save()

        inscricao.save()

        messages.success(request, f'Alterou o seu check-in no evento com sucesso!')

        return redirect('Inscricao:part_list_inscricao')

    context = {
        'QAA': QAA,
        'checkin': checkin,

    }
    return render(request, 'inscricao/participantes/inscricao_update.html', context)


def PartAlterarInscricao(request, id):
    inscricao = Inscricao.objects.get(id=id)





    respostas = Resposta.objects.filter(inscricaoid=inscricao).exclude(campoid_id=28).exclude(
        campoid_id=27)

    perguntas = []

    for resposta in respostas:

        if (resposta.campoid.tipocampoid.nome == "Escolha Múltipla" or
            resposta.campoid.tipocampoid.nome == 'Dropdown'):
            print(resposta)
            resposta.campoid.respostas = Campo.objects.filter(campo_relacionado=resposta.campoid)
        perguntas.append(resposta.campoid)

    QAA = zip(perguntas, respostas)

    if request.method == "POST":
        temp_email =  request.POST.get("3")
        if Inscricao.objects.filter(eventoid=inscricao.id, email=temp_email).exists():
            messages.success(request, f'Já existe uma inscrição com este email!')
            return redirect('Inscricao:prop_list_inscricao', inscricao.eventoid.id)
        for resposta in respostas:
            perguntaid = resposta.campoid.id

            resposta_get = request.POST.get(f"{perguntaid}")

            if perguntaid == 1:  # NOME
                inscricao.nome = resposta_get
            elif perguntaid == 2:  # IDADE
                print("im here")
                inscricao.idade = resposta_get
            elif perguntaid == 3:  # EMAIL
                inscricao.email = resposta_get
            elif perguntaid == 4:  # NUMERO TELEMOVEL
                inscricao.telemovel = resposta_get
            elif perguntaid == 5:  # PROFISSAO
                inscricao.profissao = resposta_get
            resposta.conteudo = resposta_get
            resposta.save()

        inscricao.save()

        messages.success(request, f'Alterou a sua inscrição com sucesso!')

        return redirect('Inscricao:part_list_inscricao')

    context = {
        'QAA': QAA,
    }
    return render(request, 'inscricao/participantes/inscricao_alterar.html', context)


# --------------------Views associadas aos perfil de PROPONENTE------------------------------------------------


def PropAlterarInscricao(request, id):
    inscricao = Inscricao.objects.get(id=id)





    respostas = Resposta.objects.filter(inscricaoid=inscricao).exclude(campoid_id=28).exclude(
        campoid_id=27)

    perguntas = []

    for resposta in respostas:
        if (resposta.campoid.tipocampoid.nome == "Escolha Múltipla" or
            resposta.campoid.tipocampoid.nome == 'Dropdown'):
            resposta.campoid.respostas = Campo.objects.filter(campo_relacionado=resposta.campoid)
        perguntas.append(resposta.campoid)

    QAA = zip(perguntas, respostas)

    if request.method == "POST":
        temp_email =  request.POST.get("3")
        if Inscricao.objects.filter(eventoid=inscricao.id).exists(email=temp_email):
            messages.success(request, f'Já existe uma inscrição com este email!')
            return redirect('Inscricao:prop_list_inscricao', inscricao.eventoid.id)
        for resposta in respostas:
            perguntaid = resposta.campoid.id

            resposta_get = request.POST.get(f"{perguntaid}")

            if perguntaid == 1:  # NOME
                inscricao.nome = resposta_get
            elif perguntaid == 2:  # IDADE
                print("im here")
                inscricao.idade = resposta_get
            elif perguntaid == 3:  # EMAIL
                inscricao.email = resposta_get
            elif perguntaid == 4:  # NUMERO TELEMOVEL
                inscricao.telemovel = resposta_get
            elif perguntaid == 5:  # PROFISSAO
                inscricao.profissao = resposta_get
            resposta.conteudo = resposta_get
            resposta.save()

        inscricao.save()

        messages.success(request, f'Alterou a sua inscrição com sucesso!')

        return redirect('Inscricao:prop_list_inscricao', inscricao.eventoid.id)

    context = {
        'QAA': QAA,
        'evento' : inscricao.eventoid
    }
    return render(request, 'inscricao/proponente/inscricao_alterar.html', context)


class PropConsultarInscricoes(ListView):
    # We don't have users yet. -- Implement with @Login
    # if not request.user.is_authenticated:
    #         messages.error(request, f'Por favor, faça login primeiro.')
    #         return redirect('Inscricao:list_inscricao')
    template_name = 'inscricao/proponente/list_inscricao2.html'

    paginate_by = 10

    # We don't have users yet
    def get_queryset(self):
        return Inscricao.objects.filter(eventoid=self.kwargs.get('eventoid'))


def PropRemoverInscricao(request, inscricaoid):
    # We don't have users yet.
    # if not request.user.is_authenticated:
    #         messages.error(request, f'Por favor, faça login primeiro.')
    #         return redirect('Inscricao:inscricao')

    inscricao = Inscricao.objects.get(id=inscricaoid)

    respostas = Resposta.objects.filter(inscricaoid=inscricao)

    for resposta in respostas:
        resposta.delete()

    evento = inscricao.eventoid

    evento.inscritos -= 1

    evento.save()

    inscricao.delete()

    messages.success(request, f'Eliminou a inscrição com sucesso!')

    return redirect('Inscricao:prop_list_inscricao', evento.id)


def PropAlterarEstadoInscricao(request, id):
    inscricao = Inscricao.objects.get(id=id)

    respostas = Resposta.objects.filter(inscricaoid=inscricao)

    perguntas = []

    estado = None

    for resposta in respostas:
        perguntas.append(resposta.campoid)
        if resposta.campoid.id == 27:
            estado = resposta
            estado.respostas = resposta.campoid.respostapossivelid.nome.split(",")

    QAA = zip(perguntas, respostas)

    if request.method == "POST":
        inscricao.estado = request.POST.get(f"{27}")

        inscricao.save()

        respostadb = Resposta.objects.get(inscricaoid=inscricao, campoid_id=27)

        respostadb.conteudo = request.POST.get(f"{27}")

        respostadb.save()

        messages.success(request, f'Alterou o estado da inscrição com sucesso!')

        return redirect('Inscricao:prop_list_inscricao', inscricao.eventoid.id)

    context = {
        'QAA': QAA,
        'estado': estado,

    }
    return render(request, 'inscricao/proponente/inscricao_update.html', context)


class PropConsultarCheckIns(ListView):
    # We don't have users yet. -- Implement with @Login
    # if not request.user.is_authenticated:
    #         messages.error(request, f'Por favor, faça login primeiro.')
    #         return redirect('Inscricao:list_inscricao')
    template_name = 'inscricao/checkins/list_inscricao2.html'

    paginate_by = 10

    # We don't have users yet
    def get_queryset(self):
        return Inscricao.objects.filter(eventoid=self.kwargs.get('eventoid')).filter(estado="Válida")




# ---------- PROPONENTES E PARTICIPANTES-------------------------

def consultarInscricaoPart(request, inscricaoid):
    inscricao = Inscricao.objects.get(id=inscricaoid)

    respostas = Resposta.objects.filter(inscricaoid=inscricao).exclude(campoid_id=28)  ##checkin answer

    context = {
        'inscricao': respostas,
    }

    return render(request, 'inscricao/inscricao_consultar_part.html', context)


def consultarInscricaoProp(request, inscricaoid):
    inscricao = Inscricao.objects.get(id=inscricaoid)

    respostas = Resposta.objects.filter(inscricaoid=inscricao)

    context = {
        'inscricao': respostas,
        'evento' : inscricao.eventoid
    }

    return render(request, 'inscricao/inscricao_consultar_prop.html', context)


# ------------------------- AUXILIAR FUNCTIONS FOR AJAX CALLS --------------------
#s
#
def returnCurrentEstado(request, id):
    ##TODO - validation on the ID argument


    if request.method == "GET" :
        data = {
            "estado": Inscricao.objects.get(id=id).estado,
        }
        return JsonResponse(data)

def updateEstado(request, id):
    ##TODO - validation on the ID argument


    if request.method == "POST" :

        inscricao =  Inscricao.objects.get(id=id)
        # print(f"Previous inscricao is {inscricao.estado}" )
        inscricao.estado = request.POST.get("selectedEstado")
        # print(f"Updated inscricao is {inscricao.estado}")
        inscricao.save()
        messages.success(request, "Alterou o estado da inscrição com successo.")
        return JsonResponse({'status': 'ok', 'message':'guardado com sucesso'}, status=200)


def doCheckin(request, id):
    ##TODO - validation on the ID argument

    if request.method == "POST" :

        inscricao =  Inscricao.objects.get(id=id)
        # print(f"Previous inscricao is {inscricao.estado}" )
        inscricao.checkin = request.POST.get("checkin")
        # print(f"Updated inscricao is {inscricao.estado}")
        inscricao.save()
        if inscricao.checkin == "True" :
            check = "Check in"
        else  :
            check = "Check out"
        messages.success(request, f"{check} realizado com successo.")
        return JsonResponse({'status': 'ok', 'message':'guardado com sucesso'}, status=200)
