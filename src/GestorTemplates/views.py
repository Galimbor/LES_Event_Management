from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import *
from Utilizadores.models import User, Gcp
from django.core import serializers
import json
from django.http import JsonResponse

from django.contrib import messages

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
        categoria = Tipoformulario.objects.all()[:3] #TODO
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

class FormHandling():

    #Obtem todos os campos do formulario
    def get_campos(self, formID):
        campoIDs = CampoFormulario.objects.filter(formularioid = formID).values_list('campoid')
        campos = Campo.objects.filter(id__in=campoIDs)
        return campos


    def campos_to_json(self, formID):
        todos_campos_form = self.get_campos(formID) #todos os campos incluindo os da escolha multipla
        campos = todos_campos_form.filter(campo_relacionado = None) #campos parent
        for campo in campos:
            if campo.obrigatorio == b'\x01':
                campo.obrigatorio = True
            else:
                campo.obrigatorio = False
        return serializers.serialize("json",campos)

    
    def subcampos_to_json(self, formID):
        todos_campos_form = self.get_campos(formID) #todos os campos incluindo os da escolha multipla
        campos = todos_campos_form.filter(campo_relacionado__gt = 0) #campos filho (opcoes de escolha ...)
        printspecial(campos)
        for campo in campos:
            if campo.obrigatorio == b'\x01':
                campo.obrigatorio = True
            else:
                campo.obrigatorio = False
        return serializers.serialize("json",campos)
    
    def saveCampos(self, campos):
        if(campos):
            # c = Campos.objects.filter()
            printspecial(campos)
        else:
            printspecial(campos)

    
    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            if self.request.method == 'POST':
                objects_dict = json.loads(self.request.body)
                printspecial(objects_dict)
                ## 1. Save Formulario fields
                formulario = objects_dict['formulario'] 
                f  = Formulario.objects.filter(pk=formulario['pk'])
                f.update(**formulario['fields'])
                ## 2. Save Campos fields
                campos = objects_dict['campos']
                self.saveCampos(campos)
                    
                ##TODO campos, tipo de campos, relacao campoformulario

                print(f[0].nome)
        return JsonResponse({'Save': 'Ok'})

        return super().post(*args, **kwargs)



class FormCreate(FormHandling, CreateView):
    model = Formulario
    fields = ['id']
    template_name = 'GestorTemplates/editar_formulario.html'
    success_url = reverse_lazy('form-list')

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        #templates
        template_form_queryset = Formulario.objects.filter(is_template = 1) #search for templates
        template_formID =  self.kwargs['template_form_id']
        formType = self.kwargs['form_type']
        #create form based on a selected template
        if template_formID and formType:
            form = template_form_queryset.get(id = template_formID) # search for the specific template (event, inscricao, ...)
            # create new based on the template        TODO missing clone questions as well    
            # form.pk = None #django create new object by deleting his pk and the clone it
            # form.save()
        #new empty form --> selecting type of form (evento, inscricao, ...)
        elif template_formID and not formType:
            form = Formulario.objects.create(tipoformularioid = formType )
        # create empty form without selecting type of form 
        else :
            gcp = Gcp.objects.get(id = self.request.user.id)
            form = Formulario.objects.create(gcpid = gcp) ##TODO check campos obrigatrioressss ##TODO check utilizadores
        context['tipos_campo'] = Tipocampo.objects.all()
        context['formulario_json'] = serializers.serialize("json", [form])
        context['campos_json'] = self.campos_to_json(form.id)
        context['subcampos_json'] = self.subcampos_to_json(form.id)
        context['tipos_campo_json'] = serializers.serialize("json", Tipocampo.objects.all())
        return context




class FormUpdate(FormHandling, UpdateView):
    model = Formulario
    fields = ['id']
    template_name = 'GestorTemplates/editar_formulario.html'


    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_object()
        # form = Formulario.objects.get(pk=formID) #returns one object (equivalente ao de cima)
        
        #Serialize Form
        context['tipos_campo'] = Tipocampo.objects.all()
        context['formulario_json'] = serializers.serialize("json", [form])
        context['campos_json'] = self.campos_to_json(form.id)
        context['subcampos_json'] = self.subcampos_to_json(form.id)
        context['tipos_campo_json'] = serializers.serialize("json", Tipocampo.objects.all())

        return context

    







class FormDelete(DeleteView):
    model = Formulario
    success_url = reverse_lazy('form-list')

    def get(self, request, *args, **kwargs):

        form = self.get_object()
        # if (form.is_template):
        #     # messages.add_message(request, messages.WARNING, 'Não pode eliminar formulários que são templates')
        #     return redirect(reverse_lazy('form-list'))
        return self.post(request, *args, **kwargs)




# def delete_form(request, pk):
#     if request.user:
#         Formulario.objects.get(pk=pk).delete()
#     return redirect(reverse_lazy('form-list'))