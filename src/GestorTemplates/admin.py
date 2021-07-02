from django.contrib import admin
from django.apps import apps

# Register your models here.


from .models import *


class QuestionInline(admin.TabularInline):
    extra = 1
    model = CampoFormulario


@admin.register(Formulario)
class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'updated','created')

    inlines = [
         QuestionInline,
     ]

@admin.register(Tipocampo)
class TipoCampoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'get_template')

    def get_template(self, obj):
        exist = 'no'
        if obj.template:
            exist = 'yes'
        return exist


@admin.register(Campo)
class CampoAdmin(admin.ModelAdmin):
    list_filter = ('tipocampoid',)
    list_display = ('id', 'conteudo', 'tipocampoid', 'campo_relacionado','position_index' , 'get_obrigatorio')

    
    def get_obrigatorio(self, obj):
        exist = False
        if obj.obrigatorio == b'\x01':
            exist = True
        return exist

@admin.register(CampoFormulario)
class CampoFormularioAdmin(admin.ModelAdmin):
    list_filter = ('formularioid', )
    list_display = ('formularioid', 'campoid')


    
@admin.register(EventoFormulario)
class EventoFormularioAdmin(admin.ModelAdmin):
    list_display = ('eventoid', 'formularioid')


    

models = apps.get_models()
for model in models:
    if ('GestorTemplates' in str(model)) :
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass