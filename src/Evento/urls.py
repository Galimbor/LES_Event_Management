from django.urls import path
from .views import  eventos

app_name = 'Evento'

urlpatterns = [

    path('all/', eventos, name='list_eventos'),
]
