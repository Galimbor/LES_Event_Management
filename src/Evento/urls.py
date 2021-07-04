from django.urls import path
from .views import home_view, eventos, create_logistic, meus_eventos, gerir, select_type, create_event, \
    eventos_gerir, equip_logistic, espaco_logistic, servico_logistic, submit_logistic, view_logisticas, \
    view_event, ajax_filter_type, ajax_filter_state, delete_event, edit_event, ajax_finalizar_logistica, \
    validar_evento, delete_logistica, edit_logistica, edit_espaco, edit_servico, edit_equipamento, \
    select_form, submeter_event, aceitar_event, view_my_event, recusar_evento, evento_insc

app_name = 'Evento'

urlpatterns = [
    path('', home_view, name='homeview'),
    path('all/', eventos, name='eventos'),
    path('myevents/', meus_eventos, name='meus-eventos'),
    path('gerir/<int:event_id>', gerir, name='gerir'),
    path('gerir/', eventos_gerir, name='eventos-gerir'),
    path('new/', select_type, name='select_type'),
    path('new/form/<int:type_id>', select_form, name='select_form'),
    path('new/create/<int:type_id>/<int:type_evento>', create_event, name='create-event'),
    path('new/submit/<int:event_id>', submeter_event, name='submeter-event'),
    path('new/aceitar/<int:event_id>', aceitar_event, name='aceitar-event'),
    path('new2/<int:event_id>', create_logistic, name='create-event2'),
    path('new2/equip/<int:event_id>', equip_logistic, name='equip-logistic'),
    path('new2/espaco/<int:event_id>', espaco_logistic, name='espaco-logistic'),
    path('new2/servico/<int:event_id>', servico_logistic, name='servico-logistic'),
    path('new2/submit_logistic/<int:event_id>', submit_logistic, name='submit-logistic'),
    path('gerir/view-logistic/<int:event_id>', view_logisticas, name='view-logistic'),
    path('gerir/validar-evento/<int:event_id>', validar_evento, name='validar-evento'),
    path('gerir/recusar-evento/<int:event_id>', recusar_evento, name='recusar-evento'),
    path('view/<int:event_id>', view_event, name='view-event'),
    path('view-my/<int:event_id>', view_my_event, name='view-my-event'),
    path('ajax/', ajax_filter_type, name='ajax-filter-type'),
    path('ajax/state', ajax_filter_state, name='ajax-filter-state'),
    path('ajax/finalizar_logistica', ajax_finalizar_logistica, name='ajax-finalizar-logistica'),
    path('delete/<int:event_id>', delete_event, name='delete-event'),
    path('delete-logistica/<int:event_id>', delete_logistica, name='delete-logistica'),
    path('edit/<int:event_id>', edit_event, name='edit-event'),
    path('edit-logistica/<int:event_id>', edit_logistica, name='edit-logistica'),
    path('edit-espaco/<int:event_id>', edit_espaco, name='edit-espaco'),
    path('edit-espaco/<int:event_id>/<int:espaco_id>/<str:tipo>', edit_espaco, name='edit-espaco'),
    path('edit-servico/<int:event_id>', edit_servico, name='edit-servico'),
    path('edit-equipamento/<int:event_id>', edit_equipamento, name='edit-equipamento'),

    path('evento-insc/<int:event_id>', evento_insc, name='evento-insc'),
]
