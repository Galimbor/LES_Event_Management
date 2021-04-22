from django.urls import path
from .views import registar


app_name = 'Utilizadores'


urlpatterns = [
    path('registar/', registar, name='registar'),
]       
