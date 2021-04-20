from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Recurso


# Create your views here.

def home(request):
    return render(request, 'inicio.html')


def create_recurso(request):
    return render(request, 'Recurso/new_recurso.html')


class RecursoList(ListView):
    model = Recurso
    paginate_by = 10


class RecursoCreate(CreateView):
    model = Recurso
    fields = ['id']
    template_name = 'Recurso/create_recurso.html'
    success_url = reverse_lazy('recurso-list')


class RecursoDelete(DeleteView):
    model = Recurso
    success_url = reverse_lazy('recurso-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
