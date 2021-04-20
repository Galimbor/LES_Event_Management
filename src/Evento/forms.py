from django import forms

from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.forms.widgets import SelectDateWidget

from .models import Evento

class EventoForm(forms.ModelForm):
    data_i=forms.DateField(widget = AdminDateWidget())
    hora_i = forms.TimeField(widget = AdminTimeWidget())
    data_f=forms.DateField(widget = AdminDateWidget())
    hora_f = forms.TimeField(widget = AdminTimeWidget())
    class Meta:
        model = Evento 
        fields = [
            'nome',
            'descricaogeral',
            'maxparticipantes',
        ]

