from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.contrib.admin.widgets import AdminDateWidget


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator], widget=forms.TextInput(attrs={'class': "input-clean"}))
    username = forms.CharField(label='username', max_length=100 , widget=forms.TextInput(attrs={'class': "input-clean"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "input-clean"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "input-clean"}))
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]