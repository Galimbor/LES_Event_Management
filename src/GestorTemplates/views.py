from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import *
from Utilizadores.models import User
from django.core import serializers
import json
from django.http import JsonResponse

# Apenas para demonstração. Esta view não deve estar na app forms_manager
def home(request):
    return render(request, 'inicio.html')

### print
def printspecial(var):
    print(var, "\n\n\n\n\n\n\n\n\n\n\n\n")


### USER FUNCTIONS ###
def get_user(request):
    return User.objects.filter(email = request.user.email).first()

### FORM ###
def create_form(request):
    return render(request, 'GestorTemplates/new_form.html')


class FormList(ListView):
    model = Formulario
    paginate_by = 10 
    template_name = 'GestorTemplates/lista_formularios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tiposForm = Tipoformulario.objects.all() 
        context['tiposForm'] = tiposForm
        return context

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     user = get_user(self.request)
    #     if not user or user.gcpid == None:
    #         qs = super().get_queryset().none()
    #     return qs


    # def get(self, request, *args, **kwargs):
    #     response = super().get(request, *args, **kwargs)
    #     user = get_user(self.request)
    #     return response


class FormCreate(CreateView):
    model = Formulario
    fields = ['id']
    template_name = 'GestorTemplates/editar_formulario.html'
    success_url = reverse_lazy('form-list')

    def campos_to_json(self):
        campos = Campo.objects.all()
        for campo in campos:
            if campo.obrigatorio == b'\x01':
                campo.obrigatorio = True
            else:
                campo.obrigatorio = False
        return serializers.serialize("json",campos)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = Formulario.objects.first() #TODO select the right form
       
        context['tipos_campo'] = Tipocampo.objects.all()
        context['formulario_json'] = serializers.serialize("json", [form])
        context['campos_json'] = self.campos_to_json()
        context['tipos_campo_json'] = serializers.serialize("json", Tipocampo.objects.all())
        
        return context

    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            if self.request.method == 'POST':
                print(json.loads(self.request.body))
                return JsonResponse({'status': 200})
        return super().post(*args, **kwargs)

class FormDelete(DeleteView):
    model = Formulario
    success_url = reverse_lazy('form-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def delete_form(request, pk):
    if request.user:
        Formulario.objects.get(pk=pk).delete()
    return redirect(reverse_lazy('form-list'))