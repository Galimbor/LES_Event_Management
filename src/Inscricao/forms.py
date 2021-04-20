from django import forms
from .models import Inscricao
from django.core.validators import EmailValidator


class InscricaoForm(forms.ModelForm):
    # # these two attributes above are used to override the ones directly retrieved from the model
    # # we can then use widgets to customize them
    # title = forms.CharField(widget=forms.TextInput(
    #     attrs={"placeholder": "introduce ur title"}))
    # # email = forms.EmailField()
    # description = forms.CharField(widget=forms.Textarea(
    #     attrs={
    #         "class": "new-class two",
    #         "id": "my-id-for-text-are",
    #         "rows": 20,
    #         "cols": 50,
    #         "placeholder": "introduce ur description",
    #     }))
    # price = forms.DecimalField(initial=199.99)
    email = forms.EmailField(validators=[EmailValidator])
    telemovel = forms.IntegerField(widget=forms.TextInput)
    idade = forms.IntegerField(widget=forms.TextInput)

    # associated the form with fields belonging to the model
    class Meta:
        model = Inscricao
        fields = [
            'nome',
            'email',
            'idade',
            'profissao',
            'telemovel',
        ]

    # # custom validation fuction, always need to use clean_{{attribute_name}}
    def clean_idade(self):
        idade = self.cleaned_data.get("idade")
        if idade <= 0 | idade >= 120:
            raise forms.ValidationError("A idade inserida não é válida.")
        else:
            return idade

    def clean_telemovel(self):
        telemovel = self.cleaned_data.get("telemovel")
        s_telemovel = str(telemovel)
        if len(s_telemovel) != 9:
            raise forms.ValidationError("O número de telemóvel inserido não é válido.")
        else:
            return telemovel

# # a django form that's not linked to any model
# class RawProductForm(forms.Form):
#     title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "introduce ur title"}))
#     description = forms.CharField(widget=forms.Textarea(
#         attrs={
#             "class": "new-class two",
#             "id": "my-id-for-text-are",
#             "rows": 20,
#             "cols": 50,
#             "placeholder": "introduce ur description",
#         })
#     )
#     price = forms.DecimalField()
