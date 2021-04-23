from django.urls import path
from .views import registar, login, logout_view


app_name = 'Utilizadores'


urlpatterns = [
    path('registar/', registar, name='registar'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
]       
