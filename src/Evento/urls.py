from django.urls import path
from .views import home_view, eventos, create_event2, meus_eventos, gerir, select_type, create_event, eventos_gerir

app_name = 'Evento'

urlpatterns = [
    path('', home_view, name='homeview'),
    path('all/', eventos, name='eventos'),
    path('myevents/', meus_eventos, name='meus-eventos'),
    path('gerir/<int:event_id>', gerir, name='gerir'),
    path('gerir/', eventos_gerir, name='eventos-gerir'),
    path('new/', select_type, name='select_type'),
    path('new/create/<int:type_id>', create_event, name='create-event'),
    path('new2/<int:event_id>', create_event2, name='create-event2'),
]
