from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import *
from Utilizadores.models import User, Gcp
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
        # tiposForm = Tipoformulario.objects.all()
        template = Formulario.objects.filter(is_template = 1)
        categoria = Tipoformulario.objects.all()[:3]
        context['tiposForm'] = template
        # context['categorias'] = caterogias_tipo_formulario
        context['categorias'] = categoria

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

    def campos_to_json(self, formID):
        campoIDs = CampoFormulario.objects.filter(formularioid = formID).values_list('campoid')
        campos = Campo.objects.filter(id__in=campoIDs)
        for campo in campos:
            if campo.obrigatorio == b'\x01':
                campo.obrigatorio = True
            else:
                campo.obrigatorio = False
        return serializers.serialize("json",campos)

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        #templates
        template_form = Formulario.objects.filter(is_template = 1) #search for templates
        formID =  self.kwargs['form_id']
        formType = self.kwargs['form_type']
        #create form based on a selected template
        if formID and formType:
            form = template_form.get(id = formID) # search for the specific template (event, inscricao, ...)
        #new empty form --> selecting type of form (evento, inscricao, ...)
        elif formID and not formType:
            form = Formulario.objects.create(tipoformularioid = formType )
        # create empty form without selecting type of form 
        else :
            gcp = Gcp.objects.get(id = self.request.user.id)
            form = Formulario.objects.create(gcpid = gcp) ##TODO check campos obrigatrioressss ##TODO check utilizadores
        context['tipos_campo'] = Tipocampo.objects.all()
        context['formulario_json'] = serializers.serialize("json", [form])
        context['campos_json'] = self.campos_to_json(form.id)
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