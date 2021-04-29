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


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = [
            'nome',
            'descricao',
            'unidadeorganicaid',
            'espacoid',
        ]


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            'nome',
            'descricao',
            'unidadeorganicaid',
        ]


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


class EdificioForm(forms.ModelForm):
    class Meta:
        model = Edificio
        fields = [
            'nome',
            'localizacao',
            'campusid'
        ]


class UnidadeOrganicaForm(forms.ModelForm):
    class Meta:
        model = Unidadeorganica
        fields = [
            'nome',
            'universidadeid'
        ]


class UniversidadeForm(forms.ModelForm):
    class Meta:
        model = Universidade
        fields = [
            'nome',
            'localizacao'
        ]


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = [
            'nome',
            'universidadeid'
        ]
