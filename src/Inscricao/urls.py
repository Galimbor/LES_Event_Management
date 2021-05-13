from django.urls import path

import Inscricao.views
from .views import CriarInscricao, PartConsultarInscricoes, PartInscricaoCancelar,\
    PropAlterarEstadoInscricao, PropConsultarInscricoes, PropRemoverInscricao,  PartInscricaoCheckin, PartAlterarInscricao, consultarInscricao

app_name = 'Inscricao'

urlpatterns = [



    # URL'S para os participantes
    path('create/<int:eventoid>/', CriarInscricao, name='create_inscricao'),
    path('', PartConsultarInscricoes.as_view(), name='part_list_inscricao'),
    path('evento/<int:eventoid>', PropConsultarInscricoes.as_view(), name='prop_list_inscricao'),
    path('delete/<int:inscricaoid>/', PartInscricaoCancelar, name='part_delete_inscricao'),
    path('evento/delete/<int:inscricaoid>/', PropRemoverInscricao, name='prop_delete_inscricao'),
    path('evento/update/<int:id>/', PropAlterarEstadoInscricao, name='prop_update_inscricao'),
    path('update/<int:id>/', PartInscricaoCheckin, name='part_update_inscricao'),
    path('alterar/<int:id>', PartAlterarInscricao, name='part_alterar_inscricao'),

    #URL'S para os proponentes


    #URL's para ambos
    path('consultar/<int:inscricaoid>', consultarInscricao, name='consultar_inscricao')

]
