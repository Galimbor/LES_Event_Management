from django.contrib import admin

# Register your models here.

# from .models import Formulario
# admin.site.register(Formulario)


from .models import Formulario, Campo

# Register your models here.

class QuestionInline(admin.TabularInline):
    extra = 1
    model = Campo


# @admin.register(Formulario)
# class FormAdmin(admin.ModelAdmin):
#     inlines = [
#         QuestionInline,
#     ]