from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from GestorTemplates.models import Tipoformulario, Formulario, CampoFormulario, Resposta, Campo
from .forms import InscricaoForm, InscricaoUpdateForm, InscricaoCheckinUpdateForm
from Evento.models import Evento
from .models import Inscricao
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView


# -------- Views associadas ao perfl de PARTICIPANTES -----------------------------------------------------

# TODO : fazer uma outra versão para utilizadores autenticados
def CriarInscricao(request, eventoid):
    evento = Evento.objects.get(id=eventoid)

    if evento.inscritos == evento.maxparticipantes:
        messages.success(request, f'O número máximo de inscritos foi atingido.')

        return redirect('Evento:eventos')

    # Associado à inscrição
    tipoformulario = Tipoformulario.objects.get(id=1)

    formularioInscricao = Formulario.objects.filter(eventoid=evento, tipoformularioid=tipoformulario)

    # print(formularioInscricao)

    perguntas = CampoFormulario.objects.filter(formularioid=formularioInscricao[0]).exclude(campoid_id=28).exclude(
        campoid_id=27)

    for pergunta in perguntas:
        if pergunta.campoid.tipocampoid.nome == 'RadioBox' or \
                pergunta.campoid.tipocampoid.nome == 'Dropdown':
            pergunta.campoid.respostas = pergunta.campoid.respostapossivelid.nome.split(",")

    if request.method == 'POST':

        # TODO : Aqui deve acontecer alguma validação dos campos submetidos

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

    context = {
        'form': perguntas
    }
    return render(request, 'inscricao/participantes/inscricao_create.html', context)


# TODO: melhorar a consulta com filtros e barra de procura
class PartConsultarInscricoes(ListView):
    # We don't have users yet.
    # if not request.user.is_authenticated:
    #         messages.error(request, f'Por favor, faça login primeiro.')
    #         return redirect('Inscricao:list_inscricao')

    template_name = 'inscricao/participantes/list_inscricao.html'

    paginate_by = 10

    def get_queryset(self):
        return Inscricao.objects.all()

    # Show the inscricoes of the users
    # def get_queryset(self):
    #     return Inscricao.objects.filter(userid=self.request.user)


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
    messages.success(request, f'Eliminou a sua sucessão com sucesso!')

    return redirect('Inscricao:part_list_inscricao')
    # return render(request, 'inscricao/participantes/list_inscricao.html')


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

        respostadb = Resposta.objects.get(inscricaoid=inscricao,campoid_id=28)

        if request.POST.get(f"{28}") == 'Vou' :
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
        if resposta.campoid.tipocampoid.nome == 'RadioBox' or \
                resposta.campoid.tipocampoid.nome == 'Dropdown':
            resposta.campoid.respostas = resposta.campoid.respostapossivelid.nome.split(",")
        perguntas.append(resposta.campoid)

    QAA = zip(perguntas, respostas)

    if request.method == "POST":

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

class PropConsultarInscricoes(ListView):
    # We don't have users yet. -- Implement with @Login
    # if not request.user.is_authenticated:
    #         messages.error(request, f'Por favor, faça login primeiro.')
    #         return redirect('Inscricao:list_inscricao')
    template_name = 'inscricao/proponente/list_inscricao.html'

    paginate_by = 10

    # We don't have users yet
    def get_queryset(self):
        return Inscricao.objects.filter(userid=self.request.GET.get('eventoid'))


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

    return redirect('Inscricao:prop_list_inscricao', evento.id )




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


#---------- PROPONENTES E PARTICIPANTES-------------------------

def consultarInscricao(request, inscricaoid):

    inscricao = Inscricao.objects.get(id=inscricaoid)

    respostas = Resposta.objects.filter(inscricaoid=inscricao)

    context = {
        'inscricao' : respostas,
    }

    return render(request, 'inscricao/inscricao_consultar.html', context)

