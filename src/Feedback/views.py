from django.shortcuts import render, redirect
from django.views.generic import ListView
from GestorTemplates.models import Formulario, Tipoformulario, CampoFormulario, Resposta
from Evento.models import Evento
from .models import Feedback
from django.contrib import messages


# Create your views here.
def createFeedback(request, eventoid):
    evento = Evento.objects.get(id=eventoid)

    # Associado ao feedback
    tipoformulario = Tipoformulario.objects.get(id=2)

    formularioFeedback = Formulario.objects.filter(eventoid=evento, tipoformularioid=tipoformulario)

    perguntas = CampoFormulario.objects.filter(formularioid=formularioFeedback[0])

    for pergunta in perguntas:
        if pergunta.campoid.tipocampoid.nome == 'RadioBox' or \
                pergunta.campoid.tipocampoid.nome == 'Dropdown':
            pergunta.campoid.respostas = pergunta.campoid.respostapossivelid.nome.split(",")

    print(request.POST)

    if request.method == 'POST':
        respostas = []
        feedback = Feedback(eventoid=evento)
        for pergunta in perguntas:
            # print(pergunta.campoid.id)
            resposta = request.POST.get(f"{pergunta.campoid.id}")
            respostas.append(Resposta(conteudo=resposta, feedbackid=feedback,campoid=pergunta.campoid))
            print(resposta)
        feedback.descricao = "Not sure what I'm doing"
        feedback.save()
        for resposta in respostas:
            resposta.save()

        messages.success(request, f'Submeteu o feedback com sucesso!')

        return redirect('Evento:list_eventos')

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
        print(resposta.campoid)
        perguntas.append(resposta.campoid)

    QAA = zip(perguntas, respostas)


    context = {
        'QAA': QAA,
        'feedback': feedback,
    }
    return render(request, 'feedback/view_feedback.html', context)


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
