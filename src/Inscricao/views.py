from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import InscricaoForm, InscricaoUpdateForm, InscricaoCheckinUpdateForm
from Evento.models import Evento
from .models import Inscricao
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView



#-------- Views associadas ao perfl de PARTICIPANTES -----------------------------------------------------

def CriarInscricao(request, eventoid):
    form = InscricaoForm(request.POST or None)

    if form.is_valid():
        eventoid = Evento.objects.get(id=eventoid)

        num_inscricao = eventoid.inscritos + 1

        eventoid.inscritos = eventoid.inscritos + 1
        eventoid.save()

        if eventoid.val_inscritos:
            estado = "Pendente"
        else:
            estado = "Confirmado"
        # We don't have users implemented yet.
        # if request.user.is_authenticated:
        #     userid = request.user
        # We don't have users yet.
        # if not Inscricao.objects.filter(userid=userid).filter(eventoid=eventoid):
        #     if True:
        #         messages.error(request, f'Já se encontra inscrito no evento.')
        #         return redirect('Evento:list_eventos')

        nome = form.cleaned_data.get('nome')
        email = form.cleaned_data.get('email')
        idade = form.cleaned_data.get('idade')
        telemovel = form.cleaned_data.get('telemovel')
        profissao = form.cleaned_data.get('profissao')
        checkin = 0

        userid = None

        inscricao = Inscricao(nome=nome, email=email, idade=idade, telemovel=telemovel, profissao=profissao,
                              eventoid=eventoid, userid=userid, estado=estado, num_inscricao=num_inscricao, checkin= checkin)

        inscricao.save()

        messages.success(request, f'Inscreveu-se com sucesso no evento.')

        return redirect('Evento:eventos')
    else:
        print(form.errors)

    context = {
        'form': form
    }
    return render(request, 'inscricao/participantes/inscricao_create.html', context)


class PartConsultarInscricao(ListView):
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


class PartInscricaoCancelar(DeleteView):
    model = Inscricao
    success_url = reverse_lazy('Inscricao:part_list_inscricao')

    def get(self, request, *args, **kwargs):
        messages.success(request, f'Já não se encontra inscrito no evento.')
        inscricaoid = self.kwargs.get('pk')
        inscricao = Inscricao.objects.get(id=inscricaoid)
        evento = Evento.objects.get(id=inscricao.eventoid.id)
        evento.inscritos = evento.inscritos - 1
        evento.save()
        return self.post(request, *args, **kwargs)



def PartInscricaoCheckin(request, id):
    inscricao = Inscricao.objects.get(id=id)

    form = InscricaoCheckinUpdateForm(request.POST or None)



    if form.is_valid():


        inscricao.checkin = form.cleaned_data.get('checkin')

        inscricao.save()

        messages.success(request, f'Alterou o seu check-in no evento com sucesso!')

        return redirect('Inscricao:part_list_inscricao')

    context = {
        'form': form,
        'inscricao': inscricao
    }
    return render(request, 'inscricao/participantes/inscricao_update.html', context)


class PartAlterarInscricao(UpdateView):
    template_name = 'inscricao/participantes/inscricao_alterar.html'
    form_class = InscricaoForm
    queryset = Inscricao.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Inscricao, id=id_)

    def get_success_url(self):
        messages.success(self.request, f'Alterou as informações da sua inscrição com sucesso!')
        return reverse_lazy('Inscricao:part_list_inscricao')



# --------------------Views associadas aos perfil de PROPONENTE------------------------------------------------

class PropConsultarInscricao(ListView):
    # We don't have users yet. -- Implement with @Login
    # if not request.user.is_authenticated:
    #         messages.error(request, f'Por favor, faça login primeiro.')
    #         return redirect('Inscricao:list_inscricao')
    template_name = 'inscricao/proponente/list_inscricao.html'


    paginate_by = 10

    # We don't have users yet
    def get_queryset(self):
        return Inscricao.objects.filter(userid=self.request.GET.get('eventoid'))




class PropRemoverInscricao(DeleteView):
    model = Inscricao

    def get(self, request, *args, **kwargs):
        messages.success(request, f'A inscrição foi removida do evento.')
        inscricaoid = self.kwargs.get('pk')
        inscricao = Inscricao.objects.get(id=inscricaoid)
        evento = Evento.objects.get(id=inscricao.eventoid.id)
        evento.inscritos = evento.inscritos - 1
        evento.save()
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('Inscricao:prop_list_inscricao', kwargs={'eventoid': self.kwargs.get('pk')})


class PropAlterarEstadoInscricao(UpdateView):
    template_name = 'inscricao/proponente/inscricao_update.html'
    form_class = InscricaoUpdateForm
    queryset = Inscricao.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Inscricao, id=id_)

    def get_success_url(self):
        return reverse_lazy('Inscricao:prop_list_inscricao', kwargs={'eventoid': self.kwargs.get('id')})







# PARA SUBSTITUIR DEPOIS

def Eventos_GerirInscricao(request):
    # For when we implement users
    # events = Evento.objects.all().filter(estado='aceite',proponente_internoid=request.user)

    events = Evento.objects.all().filter(estado='aceite')

    context = {
        'eventos': events,
    }

    return render(request, 'evento/proponente/eventos.html', context)