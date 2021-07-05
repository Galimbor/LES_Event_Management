from django.forms import ModelForm
from .models import Notificacao

class NotificacaoForm(ModelForm):
    editable_fields = ('',)

    def __init__(self, *args, **kwargs):
        super(NotificacaoForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field_name in self.fields:
                self.fields[field_name].widget.attrs['class'] = 'input'
                if not field_name in self.editable_fields:
                    self.fields[field_name].widget.attrs['disabled'] = True
                    if field_name == 'descricao':
                        self.fields[field_name].widget.attrs['rows'] = '10'

    class Meta:
        model = Notificacao
        exclude = ("tipo",)
