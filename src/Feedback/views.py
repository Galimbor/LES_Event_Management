from django.shortcuts import render, redirect
from django.views.generic import ListView
from GestorTemplates.models import Formulario, Tipoformulario, CampoFormulario, Campo, Resposta, EventoFormulario
from Evento.models import Evento
from Utilizadores.models import User
from .models import Feedback
from django.contrib import messages
from django.utils import timezone
from Inscricao.models import Inscricao

# Create your views here.
def createFeedback(request, eventoid):

    evento = Evento.objects.get(id=eventoid)


    if  request.user.is_authenticated:
        user_django = request.user
        user = User.objects.filter(email=user_django.email)[0]

        if not Inscricao.objects.filter(eventoid=eventoid,userid=user.id).exists():
            messages.error(request, f'Precisa de estar inscrito no evento.')

            return redirect('Evento:eventos')

        elif Feedback.objects.filter(userid=user.id, eventoid=eventoid).exists():
            messages.error(request, f'Já preencheu o seu formulário de feedback para este evento.')

            return redirect('Evento:eventos')
    else:
        user = None


    # Associado ao feedback
    formularioEvento = EventoFormulario.objects.filter(eventoid=evento.id, formularioid__tipoformularioid__categoria=2)

    formularioFeedback = formularioEvento[0].formularioid

    perguntas = CampoFormulario.objects.filter(formularioid=formularioFeedback.id, campoid__campo_relacionado=None)

    for pergunta in perguntas:
        if (pergunta.campoid.tipocampoid.nome == "Escolha Múltipla" or
                pergunta.campoid.tipocampoid.nome == 'Dropdown'):
            # pergunta.campoid.respostas = pergunta.campoid.respostapossivelid.nome.split(",")
            # pergunta.campoid.respostas = Campo.objects.filter(campo_relacionado__campo__id=pergunta.campoid.id)
            pergunta.campoid.respostas = Campo.objects.filter(campo_relacionado=pergunta.campoid)
            # print(Campo.objects.filter(campo_relacionado=pergunta.campoid))
            # print(f"{pergunta.campoid.respostas}")

    if request.method == 'POST':
        respostas = []
        feedback = Feedback(eventoid=evento)
        for pergunta in perguntas:
            resposta = request.POST.get(f"{pergunta.campoid.id}")
            respostas.append(Resposta(conteudo=resposta, feedbackid=feedback, campoid=pergunta.campoid))
        feedback.descricao = f"Feedback para o evento número : {eventoid}"
        feedback.createdAt = timezone.now()
        feedback.userid = user
        feedback.save()
        for resposta in respostas:
            resposta.save()

        messages.success(request, f'Submeteu o feedback com sucesso!')

        return redirect('Evento:eventos')

    context = {
        'form': perguntas,
        'evento' : evento,
    }
    return render(request, 'feedback/feedback_create.html', context)


# Create your views here.
def viewFeedback(request, feedbackid):
    feedback = Feedback.objects.get(id=feedbackid)
    feedbacks = Feedback.objects.filter(eventoid=feedback.eventoid.id)
    count = 1
    for feed in feedbacks:
        if feed.id == feedbackid :
            feedback.number = count
            break
        count = count + 1


    respostas = Resposta.objects.filter(feedbackid=feedbackid)

    perguntas = []

    for resposta in respostas:
        perguntas.append(resposta.campoid)

    QAA = zip(perguntas, respostas)

    context = {
        'QAA': QAA,
        'feedback': feedback,
    }
    return render(request, 'feedback/view_feedback.html', context)


def viewStatistics(request, eventoid):

    formularioEvento = EventoFormulario.objects.filter(eventoid=eventoid, formularioid__tipoformularioid__categoria=2)

    formulario = formularioEvento[0].formularioid



    #Todas as perguntas associadas aos formulário
    campoform = CampoFormulario.objects.filter(formularioid=formulario.id)

    perguntas = []

    labelslist = []
    datalist = []

    perguntasNormais = []
    respostasNormais = []

    #fetched perguntas with multiple options
    for campofield in campoform:
        if campofield.campoid.campo_relacionado == None and (campofield.campoid.tipocampoid.id == 12 or campofield.campoid.tipocampoid.id == 13):
            perguntasNormais.append(campofield.campoid)
            perguntas.append(campofield.campoid)
        elif campofield.campoid.tipocampoid.id != 12 and campofield.campoid.tipocampoid.id != 13:
            campofield.campoid.respostas = Resposta.objects.filter(campoid=campofield.campoid, feedbackid__eventoid__id=eventoid)
            perguntasNormais.append((campofield.campoid)) #colocamos as perguntas normais aqui..



    for pergunta in perguntas:
        labels = []
        data = []
        respostaspossiveis =  Campo.objects.filter(campo_relacionado=pergunta.id)
        for respostapossivel in respostaspossiveis:
            labels.append(respostapossivel.conteudo)
            data.append(Resposta.objects.filter(campoid=pergunta, feedbackid__eventoid__id=eventoid,conteudo=respostapossivel).count())
        datalist.append(data)
        labelslist.append(labels)

    for perguntasNormal in perguntasNormais:
        respostasNormais.append(Resposta.objects.filter(campoid=perguntasNormal, feedbackid__eventoid__id=eventoid))



    QAA = zip(labelslist,datalist,perguntas)


    context = {
        'perguntas': perguntas,
        'QAA' : QAA,
        'perguntasNormais': perguntasNormais,
        'respostasNormais' : respostasNormais,
    }

    return render(request,'feedback/feedback_statistics.html', context)

class listFeedback(ListView):
    # We don't have users yet. -- Implement with @Login
    # if not request.user.is_authenticated:
    #         messages.error(request, f'Por favor, faça login primeiro.')
    #         return redirect('Inscricao:list_inscricao')
    template_name = 'feedback/list_feedback.html'

    paginate_by = 10

    # We don't have users yet
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # tiposForm = Tipoformulario.objects.all()
        # numberofFeedbacks = Feedback.objects.filter(eventoid=self.kwargs.get('eventoid')).count()
        # print(context['feedback_list'][0].number)
        return context


    def get_queryset(self):
        queryset = Feedback.objects.filter(eventoid=self.kwargs.get('eventoid'))
        number = 1
        for feedback in queryset:
            feedback.number = number
            number = number + 1
        return queryset

def get_user(request):
    user_django = request.user
    user = User.objects.get(email=user_django.email)
    return user


def deleteFeedback(request, feedbackid):
    # We don't have users yet.
    # if not request.user.is_authenticated:
    #         messages.error(request, f'Por favor, faça login primeiro.')
    #         return redirect('Inscricao:inscricao')

    feedback = Feedback.objects.get(id=feedbackid)

    respostas = Resposta.objects.filter(feedbackid=feedback)

    for resposta in respostas:
        resposta.delete()

    eventoid = feedback.eventoid

    feedback.delete()

    # print("what")
    messages.success(request, f'Eliminou o feedback com sucesso!')

    return redirect('Feedback:list_feedback', eventoid.id )

class ConsultarFeedbacksPendentes(ListView):
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
            return Inscricao.objects.filter(userid=realuser.id)
        else:
            return Inscricao.objects.all()

    # Show the inscricoes of the users
    # def get_queryset(self):
        # return Inscricao.objects.filter(userid=self.request.user)
