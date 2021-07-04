from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import *
from Evento.models import Tipoevento
from Utilizadores.models import User, Gcp
from django.core import serializers
import json
from django.http import JsonResponse
from django.utils import timezone
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
    template_name = 'GestorTemplates/lista_formularios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # tiposForm = Tipoformulario.objects.all()
        template = Formulario.objects.filter(is_template = 1)
        categoria = Tipoformulario.objects.all()[:3] #TODO
        context['tiposForm'] = template
        # context['categorias'] = CATEGORIAS_TIPO_FORMULARIO
        context['categorias'] = categoria

        return context


# TODO USER FORMS!!!
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
        campos = todos_campos_form.filter(campo_relacionado = None).order_by('position_index') #campos parent
        for campo in campos:
            if campo.obrigatorio == b'\x01':
                campo.obrigatorio = True
            else:
                campo.obrigatorio = False
        return serializers.serialize("json",campos)

    
    def subcampos_to_json(self, formID):
        todos_campos_form = self.get_campos(formID) #todos os campos incluindo os da escolha multipla
        campos = todos_campos_form.filter(campo_relacionado__gt = 0).order_by('position_index') #campos filho (opcoes de escolha ...)
        # printspecial(campos)
        for campo in campos:
            if campo.obrigatorio == b'\x01':
                campo.obrigatorio = True
            else:
                campo.obrigatorio = False
        return serializers.serialize("json",campos)
    
    #Cleans data for creating Campo objects
    #@returns clean dictionary for rapid object create
    def clean_form(self, campos_dict, campo=None):
        # printspecial(campos_dict)
        tipo_campo = Tipocampo.objects.get(id = campos_dict['fields']['tipocampoid'])
        campos_dict['fields']['tipocampoid'] = tipo_campo
        if campos_dict['fields']['campo_relacionado'] and campo:
            campos_dict['fields']['campo_relacionado'] = campo
            #print('tipo campo clean', campos_dict['fields']['campo_relacionado'])
        return campos_dict['fields']


    def saveSubCampos(self, subcampos, formulario, new_campo=None): 
        try:       
            for subcampo in subcampos:
                if not Campo.objects.filter(pk=subcampo['pk']).exists():
                    if(new_campo):
                        subcampo_clean = self.clean_form(subcampo, new_campo)
                    else:
                        campo_obj = Campo.objects.get(pk = subcampo["fields"]["campo_relacionado"])
                        subcampo_clean = self.clean_form(subcampo, campo_obj)
                    new_subcampo = Campo.objects.create(**subcampo_clean)      
                    CampoFormulario.objects.create(campoid = new_subcampo, formularioid = formulario)
        except:
            pass


    def updateSubCampos(self, subcampos, formulario):   
        # subcampos estao ja limpos (com o tipocampo certo??)    
        for subcampo in subcampos:
            subcampos_qs = Campo.objects.filter(pk=subcampo['pk'])
            subcampos_qs.update(**subcampo["fields"])  
            

    
    def deleteCampos(self, campo_qs, formulario):
        for campo in campo_qs:
            forms_with_this_campo = CampoFormulario.objects.filter(campoid=campo.id)
            # se o campo estiver em mais do que um formulario
            # apagamentos apenas a relacao campo_formulario
            if forms_with_this_campo.count()>1: 
                CampoFormulario.objects.filter(campoid=campo.id, formularioid=formulario).delete()      
            # caso contrario apagamos o campo definitivamente 
            else:
                Campo.objects.filter(campo_relacionado = campo).delete() 
                campo_qs.delete()


    def deleteSubCampos(self, subcampos_dict, formulario):
        for subcampo in subcampos_dict:
            if(subcampo.get("delete")):
                Campo.objects.filter(pk = subcampo["pk"]).delete()



    def saveCampos(self,  objects_dict, formulario):
        ## TODO fazer o eliminar, checkar no objeto campo delete=true --> elimin  
        campos = objects_dict['campos']
        subcampos = objects_dict['subcampos']
        if(campos):
            for campo in campos:
                campos_dict_clean = self.clean_form(campo)
                #add new Campo to Formulario
                if(not Campo.objects.filter(pk=campo['pk']).exists()):
                    new_campo = Campo.objects.create(**campos_dict_clean)
                    CampoFormulario.objects.create(campoid = new_campo, formularioid = formulario)
                    self.saveSubCampos(subcampos,formulario, new_campo)
                #update existing Campo
                else: 
                    #TODO check save subcampos
                    updated_campo  = Campo.objects.filter(pk=campo['pk'])
                    campo_formulario = CampoFormulario.objects.filter(campoid = campo['pk'], formularioid = formulario)
                    if(campo.get("delete")):
                        self.deleteCampos(updated_campo, formulario)
                    else:
                        updated_campo.update(**campos_dict_clean)
                        self.updateSubCampos(subcampos, formulario)
        self.saveSubCampos(subcampos,formulario)
        self.deleteSubCampos(subcampos, formulario)     
        #trying to save empty form ##TODO CHECK BACK LATER ON
     

    
    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            if self.request.method == 'POST':
                objects_dict = json.loads(self.request.body)
   
                ## 1. Save Formulario fields
                formulario = objects_dict['formulario'] 
                formulario['fields']['updated']=timezone.now()

                f  = Formulario.objects.filter(pk=formulario['pk'])
                           
                f.update(**formulario['fields'])
                ## 2. Save Campos fields
                # printspecial(objects_dict)
                self.saveCampos(objects_dict, f[0])
            return JsonResponse({'status': 'ok', 'message':'guardado com sucesso'}, status=200)

        return super().post(*args, **kwargs)
    


    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categorias'] = CATEGORIAS_TIPO_FORMULARIO
        categoria = Tipoformulario.objects.all()[:3] #TODO
        context['categorias'] = categoria

        context['tipos_evento'] = Tipoevento.objects.all()

        return context


class FormCreate(FormHandling, CreateView):
    model = Formulario
    fields = ['id']
    template_name = 'GestorTemplates/editar_formulario.html'
    success_url = reverse_lazy('form-list')


    #Obtem todos os campos do formulario
    def get_campos(self, formID):
        campoIDs = CampoFormulario.objects.filter(formularioid = formID).values_list('campoid')
        campos = Campo.objects.filter(id__in=campoIDs)
        return campos

    
    
    def duplicate_form(self, form):
        todos_campos_form = self.get_campos(form.pk)
        form.pk = None #django create new object by deleting his pk and the clone it
        form.save()
        form.created = timezone.now()
        form.is_template = 0
        form.nome = "Cópia de {}".format(form.nome)
        form.save()
        for campo in todos_campos_form:
            CampoFormulario.objects.create(campoid = campo, formularioid = form)



    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        #templates
        template_form_queryset = Formulario.objects.filter(is_template = 1) #search for templates
        template_formID =  self.kwargs['template_form_id']
        formType = self.kwargs['form_type']
        #create form based on a selected template
        if template_formID and formType:
            form = template_form_queryset.get(id = template_formID) # search for the specific template (event, inscricao, ...)
            # create new based on the template            
            self.duplicate_form(form)
        #new empty form --> selecting type of form (evento, inscricao, ...)
        elif not template_formID and formType:
            printspecial("heree")
            tipo_formulario = Tipoformulario.objects.get(id = formType)
            gcp = Gcp.objects.get(id = self.request.user.id)
            gcpid = gcp
            form = Formulario.objects.create(gcpid = gcp, tipoformularioid = tipo_formulario, created = timezone.now())
        # create empty form without selecting type of form 
        else :
            gcp = Gcp.objects.get(id = self.request.user.id)
            form = Formulario.objects.create(gcpid = gcp, created = timezone.now()) ##TODO check campos obrigatrioressss ##TODO check utilizadores
        
        
      
        context['tipos_campo'] = Tipocampo.objects.all()
        context['formulario'] = form
        context['formulario_json'] = serializers.serialize("json", [form])
        context['campos_json'] = self.campos_to_json(form.id)
        context['subcampos_json'] = self.subcampos_to_json(form.id)
        context['tipos_campo_json'] = serializers.serialize("json", Tipocampo.objects.all())
        context['success_url'] = reverse_lazy('edit-form',kwargs={'pk': form.id})
        return context

    # def get(self, request):
    #     return redirect



class FormUpdate(FormHandling, UpdateView):
    model = Formulario
    fields = ['id']
    template_name = 'GestorTemplates/editar_formulario.html'


    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_object()
        # form = Formulario.objects.get(pk=formID) #returns one object (equivalente ao de cima)
        
        #Serialize Form
        context['tipos_campo'] = Tipocampo.objects.all()[1:9] #TODO wrong but must be like this because of others
        context['formulario_json'] = serializers.serialize("json", [form])
        context['campos_json'] = self.campos_to_json(form.id)
        context['subcampos_json'] = self.subcampos_to_json(form.id)
        context['tipos_campo_json'] = serializers.serialize("json", Tipocampo.objects.all())

        return context

    def get(self, *args, **kwargs):
        form = self.get_object()

        # if form.tipoeventoid:
        #     messages.add_message(self.request, messages.WARNING, 'Não é possível eliminar formulários associados a eventos')
        #     return redirect(reverse_lazy('form-list'))
    
        #  #editar formularios nao pode ser possivel quando esta a ser usado 
        eventos_deste_form = EventoFormulario.objects.filter(formularioid=form).values_list('eventoid')
        if eventos_deste_form:
            messages.add_message(self.request, messages.WARNING, 'Não é possível editar formulários associados a eventos')
            return redirect(reverse_lazy('form-list'))
        campos_deste_form = CampoFormulario.objects.filter(formularioid=form).values_list('campoid')
        respostas_deste_form = Resposta.objects.filter(campoid__in=campos_deste_form, eventoid__in=eventos_deste_form.values_list('eventoid'))
        if respostas_deste_form.exists():
            messages.add_message(self.request, messages.WARNING, 'Querias.. querias... Mas este formulário tem respostas pá:')
            return redirect(reverse_lazy('form-list'))
        return super().get(*args, **kwargs)

    




class FormDelete(DeleteView):
    model = Formulario
    success_url = reverse_lazy('form-list')

    def get(self, request, *args, **kwargs):

        form = self.get_object()
        eventos_deste_form = EventoFormulario.objects.filter(formularioid=form).values_list('eventoid')
        # printspecial(eventos_deste_form)
        # TODO verificar eliminar nao funcionou

        # if form.tipoeventoid:
        #     messages.add_message(request, messages.WARNING, 'Não é possível eliminar formulários associados a eventos')
        #     return redirect(reverse_lazy('form-list'))
        # nao eliminar formularios que estao em eventos
        if eventos_deste_form:
            messages.add_message(request, messages.WARNING, 'Não é possível eliminar formulários associados a eventos')
            return redirect(reverse_lazy('form-list'))

        campos_deste_form = CampoFormulario.objects.filter(formularioid=form).values_list('campoid')
        respostas_deste_form = Resposta.objects.filter(campoid__in=campos_deste_form, eventoid__in=eventos_deste_form.values_list('eventoid'))
        if respostas_deste_form.exists():
            messages.add_message(request, messages.WARNING, 'Querias.. querias... Mas este formulário tem respostas pá:')
            return redirect(reverse_lazy('form-list'))
        return self.post(request, *args, **kwargs)




# def delete_form(request, pk):
#     if request.user:
#         Formulario.objects.get(pk=pk).delete()
#     return redirect(reverse_lazy('form-list'))