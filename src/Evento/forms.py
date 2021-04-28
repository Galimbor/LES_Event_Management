from django import forms

from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime

from .models import Evento, Logistica


class EventoForm(forms.ModelForm):
    data_i=forms.DateField(widget = AdminDateWidget())
    hora_i = forms.TimeField(widget = AdminTimeWidget())
    data_f=forms.DateField(widget = AdminDateWidget())
    hora_f = forms.TimeField(widget = AdminTimeWidget())

    class Meta:
        model = Evento 
        fields = [
        ]


class LogisticaForm(forms.ModelForm):
    data_i=forms.DateField(widget = AdminDateWidget())
    hora_i = forms.TimeField(widget = AdminTimeWidget())
    data_f=forms.DateField(widget = AdminDateWidget())
    hora_f = forms.TimeField(widget = AdminTimeWidget())
    class Meta:
        model = Logistica
        fields = [
            'nome',
        ]

