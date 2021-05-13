from django import forms

from .models import Recurso, Espaco, Equipamento, Servico, Empresa, Edificio, Unidadeorganica, Universidade, Campus


class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = [
            'nome',
            'fonte',
            'empresaid',

        ]
        widget = forms.TextInput(attrs={'class': "input-clean"})


class EspacoForm(forms.ModelForm):
    class Meta:
        model = Espaco
        fields = [
            'nome',
            'tipo',
            'capacidade',
            'mobilidade',
            'edificioid'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': "input-clean"}),
            'tipo': forms.TextInput(attrs={'class': "input-clean"}),
            'capacidade': forms.TextInput(attrs={'class': "input-clean"}),
            'mobilidade': forms.TextInput(attrs={'class': "input-clean"}),
        }


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = [
            'nome',
            'descricao',
            'unidadeorganicaid',
            'espacoid',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': "input-clean"}),
            'descricao': forms.TextInput(attrs={'class': "input-clean"}),
        }


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            'nome',
            'descricao',
            'unidadeorganicaid',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': "input-clean"}),
            'descricao': forms.TextInput(attrs={'class': "input-clean"}),
        }


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nome',
            'descricao',
            'email',
            'telefone',
            'cidade',
            'endereco',
            'codigopostal',
            'faturacao'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': "input-clean"}),
            'descricao': forms.TextInput(attrs={'class': "input-clean"}),
            'email': forms.TextInput(attrs={'class': "input-clean"}),
            'telefone': forms.TextInput(attrs={'class': "input-clean"}),
            'cidade': forms.TextInput(attrs={'class': "input-clean"}),
            'endereco': forms.TextInput(attrs={'class': "input-clean"}),
            'codigopostal': forms.TextInput(attrs={'class': "input-clean"}),
            'faturacao': forms.TextInput(attrs={'class': "input-clean"}),
        }


class EdificioForm(forms.ModelForm):
    class Meta:
        model = Edificio
        fields = [
            'nome',
            'localizacao',
            'campusid'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': "input-clean"}),
            'localizacao': forms.TextInput(attrs={'class': "input-clean"}),
        }


class UnidadeOrganicaForm(forms.ModelForm):
    class Meta:
        model = Unidadeorganica
        fields = [
            'nome',
            'universidadeid'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': "input-clean"}),
        }


class UniversidadeForm(forms.ModelForm):
    class Meta:
        model = Universidade
        fields = [
            'nome',
            'localizacao'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': "input-clean"}),
            'localizacao': forms.TextInput(attrs={'class': "input-clean"}),
        }


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = [
            'nome',
            'universidadeid'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': "input-clean"}),
        }