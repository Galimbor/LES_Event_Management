from django.contrib import admin
from django.apps import apps

# Register your models here.


from .models import Formulario, Campo, CampoFormulario


class QuestionInline(admin.TabularInline):
    extra = 1
    model = CampoFormulario


@admin.register(Formulario)
class FormAdmin(admin.ModelAdmin):
     inlines = [
         QuestionInline,
     ]


models = apps.get_models()
for model in models:
    if ('GestorTemplates' in str(model)) :
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass