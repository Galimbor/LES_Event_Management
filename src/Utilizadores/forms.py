from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.contrib.admin.widgets import AdminDateWidget


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator])
    data=forms.DateField(widget = AdminDateWidget())

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]