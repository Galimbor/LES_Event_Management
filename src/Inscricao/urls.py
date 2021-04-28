from django.urls import path

import Inscricao.views
from .views import CriarInscricao, PartConsultarInscricao, PartInscricaoCancelar,\
    PropAlterarEstadoInscricao, PropConsultarInscricao, PropRemoverInscricao, Eventos_GerirInscricao,  PartInscricaoCheckin, PartAlterarInscricao

app_name = 'Inscricao'

urlpatterns = [

    path('evento/gerir/', Eventos_GerirInscricao, name='prop_gerir_inscricoes'),

    # URL'S para os participantes
    path('create/<int:eventoid>/', CriarInscricao, name='create_inscricao'),
    path('', PartConsultarInscricao.as_view(), name='part_list_inscricao'),
    path('evento/<int:eventoid>', PropConsultarInscricao.as_view(), name='prop_list_inscricao'),
    path('delete/<int:pk>/', PartInscricaoCancelar.as_view(), name='part_delete_inscricao'),
    path('evento/delete/<int:pk>/', PropRemoverInscricao.as_view(), name='prop_delete_inscricao'),
    path('evento/update/<int:id>/', PropAlterarEstadoInscricao.as_view(), name='prop_update_inscricao'),
    path('update/<int:id>/', PartInscricaoCheckin, name='part_update_inscricao'),
    path('alterar/<int:id>', PartAlterarInscricao.as_view(), name='part_alterar_inscricao'),

    #

]
