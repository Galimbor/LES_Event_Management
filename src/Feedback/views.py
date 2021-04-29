from django.shortcuts import render

from GestorTemplates.models import Formulario, Tipoformulario, CampoFormulario
from Evento.models import Evento


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

    if request.method == 'POST':
        print(request.POST)



    # print(perguntas)

    # form = InscricaoForm(request.POST or None)
    #
    # if form.is_valid():
    #     eventoid = Evento.objects.get(id=eventoid)
    #
    #     num_inscricao = eventoid.inscritos + 1
    #
    #     eventoid.inscritos = eventoid.inscritos + 1
    #     eventoid.save()
    #
    #     if eventoid.val_inscritos:
    #         estado = "Pendente"
    #     else:
    #         estado = "Confirmado"
    #     # We don't have users implemented yet.
    #     # if request.user.is_authenticated:
    #     #     userid = request.user
    #     # We don't have users yet.
    #     # if not Inscricao.objects.filter(userid=userid).filter(eventoid=eventoid):
    #     #     if True:
    #     #         messages.error(request, f'Já se encontra inscrito no evento.')
    #     #         return redirect('Evento:list_eventos')
    #
    #     nome = form.cleaned_data.get('nome')
    #     email = form.cleaned_data.get('email')
    #     idade = form.cleaned_data.get('idade')
    #     telemovel = form.cleaned_data.get('telemovel')
    #     profissao = form.cleaned_data.get('profissao')
    #
    #     userid = None
    #
    #     inscricao = Inscricao(nome=nome, email=email, idade=idade, telemovel=telemovel, profissao=profissao,
    #                           eventoid=eventoid, userid=userid, estado=estado, num_inscricao=num_inscricao)
    #
    #     inscricao.save()
    #
    #     messages.success(request, f'Inscreveu-se com sucesso no evento.')
    #
    #     return redirect('Evento:list_eventos')

    context = {
        'form': perguntas
    }
    return render(request, 'feedback/feedback_create.html', context)
