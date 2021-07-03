from django import forms

from .models import Recurso, Espaco, Equipamento, Servico, Empresa, Edificio, Unidadeorganica, Universidade, Campus
from django.core.exceptions import NON_FIELD_ERRORS


class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = [
            'Nome',
            'fonte',
            'empresaid',

        ]
        widget = forms.TextInput(attrs={'class': "input-clean"})


class EspacoForm(forms.ModelForm):
    class Meta:
        model = Espaco
        fields = [
            'Nome',
            'tipo',
            'capacidade',
            'mobilidade',
            'edificioid'
        ]
        widgets = {
            'Nome': forms.TextInput(attrs={'class': "input-clean"}),
            'tipo': forms.TextInput(attrs={'class': "input-clean"}),
            'capacidade': forms.TextInput(attrs={'class': "input-clean"}),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Já existe um Espaço com este nome no Edifício selecionado",
            },
            'capacidade': {
                'invalid': 'A capacidade tem que ser um número inteiro positivo'
            }
        }


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = [
            'Nome',
            'descricao',
            'unidadeorganicaid',
            'espacoid',
        ]
        widgets = {
            'Nome': forms.TextInput(attrs={'class': "input-clean"}),
            'descricao': forms.TextInput(attrs={'class': "input-clean"}),
        }
        error_messages = {
            'Nome': {
                "unique": "O nome selecionado já foi atribuído a outro equipamento",
            },
            'descricao': {
            },
        }


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            'Nome',
            'Descricao',
            'unidadeorganicaid',
        ]
        widgets = {
            'Nome': forms.TextInput(attrs={'class': "input-clean"}),
            'Descricao': forms.TextInput(attrs={'class': "input-clean"}),
        }
        error_messages = {
            'Nome': {
                "unique": "O nome para este serviço já foi atribuído a outro serviço",
            },
            'Descricao': {
            },
        }


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'Nome',
            'descricao',
            'email',
            'telefone',
            'cidade',
            'endereco',
            'codigopostal',
            'faturacao'
        ]
        widgets = {
            'Nome': forms.TextInput(attrs={'class': "input-clean"}),
            'descricao': forms.TextInput(attrs={'class': "input-clean"}),
            'email': forms.TextInput(attrs={'class': "input-clean"}),
            'telefone': forms.TextInput(attrs={'class': "input-clean"}),
            'cidade': forms.TextInput(attrs={'class': "input-clean"}),
            'endereco': forms.TextInput(attrs={'class': "input-clean"}),
            'codigopostal': forms.TextInput(attrs={'class': "input-clean"}),
            'faturacao': forms.TextInput(attrs={'class': "input-clean"}),
        }
        error_messages = {
            'Nome': {
                'unique': "Já existe uma Empresa com este nome",
            },
            'email': {
                'invalid': "O endereço de email introduzido é inválido"
            },
            'telefone': {
                'invalid': "O número de telefone introduzido é inválido"
            },
            'codigopostal': {
                'invalid': "O código postal introduzido é inválido, deve ter o formato XXXX-XXX"
            },
            'faturacao': {
                'invalid': "O Número de Contribuinte introduzido é inválido"
            },
            'endereco': {
                'invalid': "O Endereço introduzido é inválido"
            },

        }


class EdificioForm(forms.ModelForm):
    class Meta:
        model = Edificio
        fields = [
            'Nome',
            'localizacao',
            'campusid'
        ]
        widgets = {
            'Nome': forms.TextInput(attrs={'class': "input-clean"}),
            'localizacao': forms.TextInput(attrs={'class': "input-clean"}),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Já existe um Edifício com este nome no Campus selecionado",
            }
        }


class UnidadeOrganicaForm(forms.ModelForm):
    class Meta:
        model = Unidadeorganica
        fields = [
            'Nome',
            'universidadeid'
        ]
        widgets = {
            'Nome': forms.TextInput(attrs={'class': "input-clean"}),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Já existe uma Unidade Orgânica com este nome na Universidade selecionada",
            }
        }


class UniversidadeForm(forms.ModelForm):
    class Meta:
        model = Universidade
        fields = [
            'Nome',
            'localizacao'
        ]
        widgets = {
            'Nome': forms.TextInput(attrs={'class': "input-clean"}),
            'localizacao': forms.TextInput(attrs={'class': "input-clean"}),
        }


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = [
            'Nome',
            'universidadeid'
        ]
        widgets = {
            'Nome': forms.TextInput(attrs={'class': "input-clean"}),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Já existe um Campus com este nome na Universidade selecionada",
            }
        }
