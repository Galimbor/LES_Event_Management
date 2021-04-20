from django.urls import path
from .views import create_inscricao

app_name = 'Inscricao'

urlpatterns = [

    path('create/<int:eventoid>/', create_inscricao, name='create_inscricao'),
]
