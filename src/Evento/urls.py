from django.urls import path
from .views import create_event, home_view, eventos

app_name = 'Evento'

urlpatterns = [
    path('', home_view, name='homeview'),
    path('all/', eventos, name='eventos'),
    path('new/', create_event, name='create-event'),
]
