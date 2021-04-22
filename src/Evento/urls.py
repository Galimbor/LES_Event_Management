from django.urls import path
from .views import create_event, home_view, eventos, create_event2, meus_eventos, gerir

app_name = 'Evento'

urlpatterns = [
    path('', home_view, name='homeview'),
    path('all/', eventos, name='eventos'),
    path('myevents/', meus_eventos, name='meus-eventos'),
    path('gerir/<int:event_id>', gerir, name='gerir'),
    path('new/', create_event, name='create-event'),
    path('new2/<int:event_id>', create_event2, name='create-event2'),
]
