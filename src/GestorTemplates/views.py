from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Formulario, Campo

# Apenas para demonstração. Esta view não deve estar na app forms_manager
def home(request):
    return render(request, 'inicio.html')


def create_form(request):
    return render(request, 'GestorTemplates/new_form.html')


class FormList(ListView):
    model = Formulario
    paginate_by = 10 


class FormCreate(CreateView):
    model = Formulario
    fields = ['title']
    template_name = 'GestorTemplates/create_form.html'
    success_url = reverse_lazy('form-list')

class FormDelete(DeleteView):
    model = Formulario
    success_url = reverse_lazy('form-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)