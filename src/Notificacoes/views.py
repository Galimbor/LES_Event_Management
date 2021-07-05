from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Notificacao
from django.utils import timezone
from django.core import serializers
import json
from .forms import NotificacaoForm



class NotificacoesList(ListView):
    model = Notificacao

    def get_queryset(self):
        estado = self.kwargs.get('estado')
        qs = super().get_queryset().filter(user=self.request.user)
        if estado:
            return qs.filter(estado=estado)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['unread_count'] = Notificacao.objects.filter(estado=1).count()
        return context
        
class NotificacoesUpdate(UpdateView):
    model = Notificacao
    form_class = NotificacaoForm
    success_url = reverse_lazy('notification-list')

    def get(self, *args, **kwargs):
        notification = self.get_object()
        notification.estado = notification.Estado.LIDO
        notification.save()
        return super().get(*args, **kwargs)

class NotificacoesDelete(DeleteView):
    model = Notificacao
    success_url = reverse_lazy('notification-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)