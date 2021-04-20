from django import forms

from .models import Recurso


class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = [
            'nome',
            'fonte',
            'empresaid',
        ]
