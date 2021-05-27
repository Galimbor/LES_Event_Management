from django.urls import path
from .views import home_view, eventos, create_logistic, meus_eventos, gerir, select_type, create_event, \
    eventos_gerir, equip_logistic, espaco_logistic, servico_logistic, submit_logistic, view_logisticas, \
    view_event, create_csv_certificates

app_name = 'Evento'

urlpatterns = [
    path('', home_view, name='homeview'),
    path('all/', eventos, name='eventos'),
    path('myevents/', meus_eventos, name='meus-eventos'),
    path('gerir/<int:event_id>', gerir, name='gerir'),
    path('gerir/', eventos_gerir, name='eventos-gerir'),
    path('new/', select_type, name='select_type'),
    path('new/create/<int:type_id>', create_event, name='create-event'),
    path('new2/<int:event_id>', create_logistic, name='create-event2'),
    path('new2/equip/<int:event_id>', equip_logistic, name='equip-logistic'),
    path('new2/espaco/<int:event_id>', espaco_logistic, name='espaco-logistic'),
    path('new2/servico/<int:event_id>', servico_logistic, name='servico-logistic'),
    path('new2/submit_logistic/<int:event_id>', submit_logistic, name='submit-logistic'),
    path('gerir/view-logistic/<int:event_id>', view_logisticas, name='view-logistic'),
    path('view/<int:event_id>', view_event, name='view-event'),
    path('gerir/criarCSV/<int:evento_id>', create_csv_certificates, name='criar-csv' ),
]
