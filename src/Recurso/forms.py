from django import forms

from .models import Recurso, Espaco, Equipamento, Servico


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
            'capacidade',
            'mobilidade',
            'recursoid'
        ]


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = [
            'nome',
            'descricao',
            'reservado',
            'recursoid',
            'unidadeorganicaid',
            'espacoid'
        ]


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            'nome',
            'reservada',
            'recursoid',
            'unidadeorganicaid',
        ]
