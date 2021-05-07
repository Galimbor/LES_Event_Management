from django.shortcuts import render, redirect
from django.views.generic import ListView
from GestorTemplates.models import Formulario, Tipoformulario, CampoFormulario, Resposta
from Evento.models import Evento
from Utilizadores.models import User
from .models import Feedback
from django.contrib import messages
from Inscricao.models import Inscricao

# Create your views here.
def createFeedback(request, eventoid):

    evento = Evento.objects.get(id=eventoid)


    if not request.user.is_authenticated:
        messages.error(request, f'Por favor autentique-se.')

        return redirect('Evento:eventos')

    user = get_user(request)

    if not Inscricao.objects.filter(eventoid=eventoid,userid=user).exists():
        messages.error(request, f'Precisa de estar inscrito no evento.')

        return redirect('Evento:eventos')



    # Associado ao feedback
    tipoformulario = Tipoformulario.objects.get(id=2)

    formularioFeedback = Formulario.objects.filter(eventoid=evento, tipoformularioid=tipoformulario)

    perguntas = CampoFormulario.objects.filter(formularioid=formularioFeedback[0])

    for pergunta in perguntas:
        if pergunta.campoid.tipocampoid.nome == 'RadioBox' or \
                pergunta.campoid.tipocampoid.nome == 'Dropdown':
            pergunta.campoid.respostas = pergunta.campoid.respostapossivelid.nome.split(",")


    if request.method == 'POST':
        respostas = []
        feedback = Feedback(eventoid=evento)
        for pergunta in perguntas:
            resposta = request.POST.get(f"{pergunta.campoid.id}")
            respostas.append(Resposta(conteudo=resposta, feedbackid=feedback, campoid=pergunta.campoid))
        feedback.descricao = "Not sure what I'm doing"
        feedback.save()
        for resposta in respostas:
            resposta.save()

        messages.success(request, f'Submeteu o feedback com sucesso!')

        return redirect('Evento:eventos')

    context = {
        'form': perguntas
    }
    return render(request, 'feedback/feedback_create.html', context)


# Create your views here.
def viewFeedback(request, feedbackid):
    feedback = Feedback.objects.get(id=feedbackid)

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


    formulario = Formulario.objects.get(tipoformularioid_id=2, eventoid=eventoid)

    #Todas as perguntas associadas aos formulário
    campoform = CampoFormulario.objects.filter(formularioid=formulario)

    perguntas = []

    labelslist = []
    datalist = []


    #fetched perguntas with multiple options
    for campofield in campoform:
        if campofield.campoid.respostapossivelid is not None:
            perguntas.append(campofield.campoid)

    for pergunta in perguntas:
        respostasxpto = Resposta.objects.filter(campoid=pergunta, feedbackid__eventoid__id=eventoid)
        respostaspossiveis = respostasxpto[0].campoid.respostapossivelid.nome.split(",")
        labels = []
        data = []
        for respostapossivel in respostaspossiveis:
            labels.append(respostapossivel)
            data.append(Resposta.objects.filter(campoid=pergunta, feedbackid__eventoid__id=eventoid,conteudo=respostapossivel).count())
        labelslist.append(labels)
        datalist.append(data)


    QAA = zip(labelslist,datalist,perguntas)


    context = {
        'perguntas': perguntas,
        'QAA' : QAA,

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
    def get_queryset(self):
        return Feedback.objects.filter(eventoid=self.kwargs.get('eventoid'))

def get_user(request):
    user_django = request.user
    user = User.objects.get(email=user_django.email)
    return user